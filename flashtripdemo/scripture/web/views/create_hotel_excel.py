import logging

import xlrd

from sanic.response import html
from web import settings
from tasks.create_hotel import dispatcher
from . import views_bp

logger = logging.getLogger(__name__)

XLSXMIME = 'application/vnd.ms-excel'
H = '''
<h2>请上传EXCEL表格</h2>
<span>格式：供应商 | id | booking网址 | TripAdvisor网址</span>
<p></p>
<form taget="_self" method="post" enctype="multipart/form-data">
选择Excel:
<input type="file" name="excel"/>
<button>解析</button>
</form>
'''


@views_bp.get("/creating/hotel")
async def crawl_hcom(request):
    return html(H)


@views_bp.post("/creating/hotel")
async def _post_create_hotel(request):
    xlsx = request.files.get('excel')
    if not xlsx:
        logger.warning(f'上传文件为空')
        return html('<h1>文件为空</h1>', status=400)
    if XLSXMIME != xlsx.type:
        logger.warning(f'文件名{xlsx.name},上传文件类型错误')
        return html("<h1>错误的文件类型</h1>")
    book = xlrd.open_workbook(file_contents=xlsx.body)
    _ori_info = book.sheet_by_index(0)
    if _ori_info.ncols < 3:
        logger.warning(f'文件名{xlsx.name},上传文件信息不完整')
        return html('<h1>信息不完整</h1>', status=400)
    hotel_info_list = []
    for index in range(_ori_info.nrows):
        supplier = _ori_info.cell_value(rowx=index, colx=0)
        hotel_id = _ori_info.cell_value(rowx=index, colx=1)
        crawl_url = _ori_info.cell_value(rowx=index, colx=2)
        if not (supplier and hotel_id and crawl_url):
            continue
        ta_url = ''
        if _ori_info.ncols >= 4:
            ta_url = _ori_info.cell_value(rowx=index, colx=3)
        hotel_info = f'{supplier}{hotel_id}'
        if hotel_info in hotel_info_list:
            continue
        hotel_info_list.append(hotel_info)
        supplier = settings.SUPPLIER_NAME_2_ID.get(supplier.strip().lower())
        data = {
            'name': '',
            'supplier': supplier,
            'hid': hotel_id,
            'website': "bk_url",
            'url': crawl_url,
            'address': '',
            'comments': '',
            'comments_url': '',
        }
        dispatcher.delay(data, ta_url)
    logger.info(f'上传了一份文件:文件名{xlsx.name},大小: {len(xlsx.body)}')
    return html(f'''<h1>文件信息</h1>
                <li>文件名: {xlsx.name}</li>
                <li>mime: {xlsx.type}</li>
                <li>文件大小: {len(xlsx.body)}</li>
                <li>有效信息: {len(hotel_info_list)}</li>''')
