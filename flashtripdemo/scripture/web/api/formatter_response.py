# coding: utf-8
import pandas
from sanic.response import json, html

def rest_result(request, dictionary: dict):
    """ensure result format by `Accept` in headers
    """
    if "application/json" in request.headers.get("Accept").lower():
        return json(dictionary, status=dictionary.get("status", 200))
    status = dictionary.pop("status", 200)
    if status != 200:
        return html(dictionary.get("errmsg") or dictionary.get('err_msg'))
    df = pandas.DataFrame.from_dict(
        {"result": dictionary}
    )  # pylint: disable=C0103
    return html(df.to_html(), status=status)
