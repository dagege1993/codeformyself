# conding: utf8

from datetime import datetime, timedelta
from io import BytesIO
import logging

import xlwt
from sanic.response import html, raw
from tasks.inventories import hotel_online_check

from web import settings
from web.utils.database import databases
from web.api.record_statitics import extract_data, save_excel

from . import views_bp


H = """<h1>下载各阶段用户点击统计excel</h1>
<h2>请使用谷歌浏览器或手动填写时间 格式如: 2018-01-01 00:00:00</h2>
<form taget="_self" method="post" enctype="multipart/form-data">
<input type="password" name="secret">身份码</input><br /><br /> 
<a /> 根据不同的浏览器版本，可能需要指定上下午 <br /><br />
<a /> ⬆/⬇切换上下午，当天0点0分会显示为 上午12:00 <br /><br /> 
<input type="datetime-local" name="start_time">查询开始日期（默认为一小时前）</input><br /><br /> 
<input type="datetime-local" name="end_time">查询结束日期（默认为当前时间）</input><br /><br /> 
<div />需要查看的阶段（可多选）<br /><br /> 
<input name="stages" type="checkbox" value="availability" />查价 
<input name="stages" type="checkbox" value="preparation" />验价（预订） 
<input name="stages" type="checkbox" value="booking" />下订（下单） 
<input name="stages" type="checkbox" value="cancellation" />取消订单 
<br /><br /> 
<button>查询并下载数据</button>
</form>
"""

stage_map = {
    'availability': '查价',
    'preparation': '验价/预订',
    'booking': '下单',
    'cancellation': '取消'
}
secret_map = {
    'weegoTrip': 'wangxue',
    'liubowen': 'liubowen',
}

@views_bp.get("/record")
async def crawl_hcom(request):
    return html(H)


@views_bp.post("/record")
async def start_crawl_hcom(request):
    logger = logging.getLogger(__name__)
    form = request.form
    secret = form.get('secret')
    if not secret or secret not in secret_map:
        return html(
            '<h1>身份验证失败，请重新访问页面</h1>'
        )
    
    start_time = form.get('start_time')
    if not start_time:
        # 后续会对时间做时区校准，在此先将默认时间设置为北京时区
        start_time = datetime.now() + timedelta(hours=7)
    end_time = form.get('end_time')
    if not end_time:
        end_time = datetime.now() + timedelta(hours=8)
    stages = form.getlist('stages', [])
    logger.info(f"start_time: {start_time}")
    logger.info(f"end_time: {end_time}")
    logger.info(f"stages: {stages}")
    logger.info(f"{secret_map[secret]} download data with conditon: \nstart_time: {start_time}\nend_time: {end_time}\nstages: {stages}")
    data = await extract_data(start_time, end_time, stages)
    wb = save_excel(data)
    excel = BytesIO()
    wb.save(excel)
    excel.seek(0)
    return raw(
        excel.getvalue(),
        headers={
            "Content-Disposition": f"attachment;filename={start_time}-{end_time}{'/'.join(stages)}.xls"
        },
        content_type="application/vnd.ms-excel",
    )
