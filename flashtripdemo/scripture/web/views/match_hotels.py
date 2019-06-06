import os
import xlrd
import logging
import requests

from sanic.response import html

from web import settings
from web.api.formatter_response import rest_result
from . import views_bp
from .privacy import template

XLSXMIME = 'application/vnd.ms-excel'
logger = logging.getLogger(__name__)
hotel_info_key = [
    "ori_hotel_name",
    "ori_hotel_provider",
    "ori_hotel_code",
    "ori_hotel_address",
    "ori_hotel_country"
]


@views_bp.get('/match/hotels')
async def match_hotel(request):
    _file = os.path.join(template, 'match.html')
    with open(_file) as f:
        content = f.read()
    return html(content)


@views_bp.post('/match/hotels')
async def _crawl_upload(request):
    ori_hotel_info = {}
    opt = request.form.get('opt')
    if not opt:
        logger.warning(f'{request}无opt,非法请求')
        return rest_result(
            request, {"status": 400, "errmsg": "非法请求"}
        )
    match_prob = request.form.get('prob')
    if opt == 'form':
        ori_hotel_name = request.form.get('name')
        if not ori_hotel_name:
            return rest_result(
                request, {"status": 400, "errmsg": "酒店名为必填项"}
            )
        ori_hotel_provider = request.form.get('provider')
        if ori_hotel_provider and ori_hotel_provider not in settings.SUPPLIER_NAME_2_ID:
            return rest_result(
                request, {"status": 400, "errmsg": "供应商有误"}
            )
        ori_hotel_code = request.form.get('code')
        ori_hotel_address = request.form.get('address')
        ori_hotel_country = request.form.get('country')
        ori_hotel_info = {
            "ori_hotel": [
                {
                    "ori_hotel_name": ori_hotel_name,
                    "ori_hotel_provider": ori_hotel_provider,
                    "ori_hotel_code": ori_hotel_code,
                    "ori_hotel_address": ori_hotel_address,
                    "ori_hotel_country": ori_hotel_country,
                }
            ]
        }
        logger.debug(f'ori_hotel_info:{ori_hotel_info}')
    elif opt == 'excel':
        excel = request.files.get('excel')
        if not excel:
            logger.info(f'{request}包含文件为空')
            return rest_result(
                request, {"status": 400, "errmsg": "文件为空"}
            )
        excel_info = f'文件名: {excel.name},mime: {excel.type}'
        logger.info(f'上传了一份文件:文件信息:{excel_info}')
        if XLSXMIME != excel.type:
            logger.info(f'{request}{excel_info} 上传了错误的文件类型')
            return rest_result(
                request, {"status": 400, "errmsg": "错误的文件类型"}
            )
        book = xlrd.open_workbook(file_contents=excel.body)
        _page = book.sheet_by_index(0)
        ori_hotel_info["ori_hotel"] = []
        for row_index in range(_page.nrows):
            one_hotel_info = {}
            for col_index, cel_value in enumerate(_page.row_values(row_index)):
                if col_index == 0 and not cel_value:
                    break
                if col_index == 1 and cel_value and cel_value not in settings.SUPPLIER_NAME_2_ID:
                    one_hotel_info = {}
                    break
                if cel_value and col_index < 5:
                    one_hotel_info[hotel_info_key[col_index]] = cel_value
            if one_hotel_info:
                ori_hotel_info["ori_hotel"].append(one_hotel_info)
        logger.debug(f'{request}上传了一份excel文件,response_dict:{ori_hotel_info}')
    ori_hotel_info['match_prob'] = match_prob
    logger.info(f'{request}开始了一次酒店匹配,原始酒店信息为:{ori_hotel_info}')
    try:
        result = requests.post(
            f'{settings.EXAMINER_API}/api/v1/match/',
            json=ori_hotel_info
        )
        if result.status_code == 200:
            logger.debug(f'result.json(){result.json()}')
            tr = ''
            if not result.json():
                return rest_result(
                    request, {"status": 200, "结果": "匹配结束无相似酒店"}
                )
            for hotel in result.json():
                _similar_hotel = hotel["similar_hotel"]
                tr += f'<tr>' \
                      f'<td>原酒店名称:{hotel["ori_hotel_name"]}</td>' \
                      f'<td>' \
                      f'相似酒店名称:{_similar_hotel["hotel_name"]},' \
                      f'供应商:{_similar_hotel["hotel_provider"]},' \
                      f'酒店ID:{_similar_hotel["hotel_code"]},' \
                      f'地址:{_similar_hotel["hotel_addr"]},' \
                      f'国家:{_similar_hotel["hotel_country"]},' \
                      f'相似率:{_similar_hotel["hotel_prob"]}' \
                      f'</td>' \
                      f'</tr>'
            table = f'<table border="1">{tr}</table>'
            return html(table)
        else:
            logger.warning(f'酒店信息:{ori_hotel_info}对应查询异常')
            return rest_result(
                request, {"status": 500, "errmsg": "查询异常"}
            )
    except Exception as exc:
        logger.warning(f"examiner api 异常", exc_info=exc)
        return rest_result(
            request, {"status": 500, "errmsg": "examiner lose effectiveness"}
        )
