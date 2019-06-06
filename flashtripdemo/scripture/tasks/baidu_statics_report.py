import json
import pandas
import requests
import os
import tempfile
import time
from celery.utils.log import get_task_logger
from datetime import datetime, timedelta

from tasks.utils.database import databases
from tasks.utils.notifiers import EmailNotifier
from tasks.application import app
from tasks import settings

logger = get_task_logger("tasks")


def _get_sem_map():
    db = databases("scripture")
    sem = db.statics.sem.find()
    result = {}
    for item in sem:
        result[f'{item["sem_name"]}={item["sem_id"]}'] = {
            "unit": item["unit"],
            "plan": item["plan"],
            "keywords": item["keywords"],
        }

    return result


def _update_sem(sem_file_path):
    db = databases("scripture")
    db.statics.sem.remove()
    with open(sem_file_path, "r") as f:
        sem = json.load(f)
        c = [
            {
                "sem_id": k.split("=")[1],
                "sem_name": k.split("=")[0],
                "unit": sem[k]["unit"],
                "plan": sem[k]["plan"],
                "keywords": sem[k]["keywords"],
            }
            for k in sem
        ]

        db.statics.sem.insert_many(c)
        logger.info("Inserted %s", db.statics.sem.count_documents({}))


def _download_event_track_data(start_date, end_date):
    """ 下载百度统计最终事件数据
    """
    URL = "https://api.baidu.com/json/tongji/v1/ReportService/getData"

    account = settings.BAIDU_STATICS.get("account", {})
    payload = {
        "header": {
            "account_type": 1,
            "password": account["password"],
            "token": account["token"],
            "username": account["username"],
        },
        "body": {
            "site_id": account["site_id"],
            "start_date": start_date,
            "end_date": end_date,
            "metrics": "event_count",
            "method": "custom/event_track/a",
        },
    }

    resp = requests.post(url=URL, json=payload)
    data = resp.json()
    if data["header"]["status"] != 0:
        logger.error("Fetch statics failed: %s", data)
        raise Exception(data["header"]["desc"])
    return data["body"]["data"][0]["result"]["items"]


def _handle_origin_data(data):
    """ 处理原始统计数据
    """
    result = []
    for index in range(0, len(data[0])):
        item = data[0][index][0]
        if not item.get("c", "").startswith("sem"):
            continue

        count = data[1][index][0]
        name = item["c"]
        action = item["a"]
        value = json.loads(item["l"])
        sem_name = name.split(":")[0]

        sem_id = value.get("v", "")
        timestamp = value.get("t", None)

        if not timestamp:
            timestamp = datetime(1970, 1, 1).timestamp * 1000

        result.append([f"{sem_name}={sem_id}", action, count, timestamp])

    return result


def _group_by_datetime(data):
    grouped_data = {}
    for index in range(len(data)):
        [sem_id, action, count, timestamp] = data[index]
        date_string = datetime.fromtimestamp(timestamp / 1000).strftime(
            "%Y-%m-%d"
        )
        if not date_string in grouped_data:
            grouped_data[date_string] = {}

        if not sem_id in grouped_data[date_string]:
            grouped_data[date_string][sem_id] = {
                "查价": 0,
                "验价": 0,
                "立即预定": 0,
                "点击提交订单": 0,
                "支付成功": 0,
            }

        if action in grouped_data[date_string][sem_id]:
            grouped_data[date_string][sem_id][action] += count

    result = []
    for date_string in grouped_data:
        for sem_id in grouped_data.get(date_string, []):
            tmp = []
            for count in grouped_data[date_string].get(sem_id, []):
                tmp.append(grouped_data[date_string][sem_id].get(count, ""))
            tmp = [date_string, sem_id] + tmp

            result.append(tmp)

    return result


def _fill_origin_data_to_dict(data):
    sem_map = _get_sem_map()

    result = {
        "日期": [],
        "code": [],
        "计划": [],
        "单元": [],
        "关键词": [],
        "查价": [],
        "验价": [],
        "立即预定": [],
        "点击提交订单": [],
        "付款完成": [],
    }

    def take_date(elem):
        return elem[0]

    data.sort(key=take_date, reverse=True)
    for index in range(len(data)):
        [
            date_string,
            sem_id,
            check_price,
            prepare,
            book,
            create_order,
            paid,
        ] = data[index]

        t = sem_map.get(sem_id, {})
        plan = t.get("plan", "")
        unit = t.get("unit", "")
        keywords = t.get("keywords", "")

        result["日期"].append(date_string)
        result["code"].append(sem_id)
        result["计划"].append(plan)
        result["单元"].append(unit)
        result["关键词"].append(keywords)
        result["查价"].append(check_price)
        result["验价"].append(prepare)
        result["立即预定"].append(book)
        result["点击提交订单"].append(create_order)
        result["付款完成"].append(paid)

    return result


def _to_excel(file_path, data):
    df = pandas.pandas.DataFrame.from_dict(data)
    df.to_excel(file_path, index=False)

    return file_path


def _notify(file_path):
    try:
        account = settings.EMAIL_ACCOUNT
        mail = EmailNotifier(**account)
        msg = mail.format_attach_message(
            f"百度统计-{os.path.basename(file_path)}",
            file_path,
            settings.BAIDU_STATICS["receivers"],
            settings.BAIDU_STATICS["from"],
        )
        mail.send(msg)

        logger.info(f"Email sended")
    except Exception as e:
        logger.exception(e)
        raise e
    finally:
        os.remove(file_path)
        logger.info(f"Temp file {file_path} was removed")


@app.task
def export_baidu_statics():
    start_date = end_date = datetime.now() - timedelta(1)
    start_date_str = datetime.strftime(start_date, "%Y-%m-%d")
    end_date_str = datetime.strftime(end_date, "%Y-%m-%d")

    logger.info(f"Start export {start_date_str}-{end_date_str} statics")

    file_path = os.path.join(
        tempfile.gettempdir(),
        f"baidu_statics_{start_date_str}_{end_date_str}_{int(time.time())}.xlsx",
    )

    logger.info(f"Temp file path:{file_path}")

    track_data = _download_event_track_data(start_date_str, end_date_str)
    handled_data = _handle_origin_data(track_data)
    grouped_data = _group_by_datetime(handled_data)
    filled_data = _fill_origin_data_to_dict(grouped_data)
    excel_path = _to_excel(file_path, filled_data)
    _notify(file_path)
