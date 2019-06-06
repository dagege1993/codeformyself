# coding: utf-8

# Standard Library
import asyncio
import logging
from enum import Enum
from typing import Any, Dict, Tuple, Optional

# Third Party
import sqlalchemy as sa
from gino import Gino
from web.utils.database import pg_databases as databases

# db = asyncio.get_event_loop().run_until_complete(databases('record'))
db = databases('record')

class PullDown(db.Model):
    __tablename__ = "pull_down"

    recordid = db.Column(
        db.Integer, primary_key=True, comment="记录ID"
    )

    cms_hotel_name = db.Column(
        db.Text, comment="酒店名称"
    )

    cms_hotel_id = db.Column(db.CHAR(24), comment="cms酒店id")

    supplier = db.Column(db.Text, comment="供应商名称")

    supplier_id = db.Column(db.CHAR(24), comment="供应商酒店ID")

    created_at = db.Column(
        db.DateTime(timezone=True), comment="创建时间",
        server_default=sa.sql.func.now()
        )

    query_time = db.Column(db.DateTime(timezone=True), comment="请求内含时间")

    checkin = db.Column(db.Text, comment="入住日期")

    checkout = db.Column(db.Text, comment="离店日期")

    is_pull_down = db.Column(db.Boolean, comment="此次请求是否需下线")

    is_pull_down_ok = db.Column(db.Boolean, comment="此次下线操作是否成功")

    request_from = db.Column(db.Text, comment="请求发起来源")

    room_type = db.Column(db.Text, comment="请求房型")

    meal_type = db.Column(db.Text, comment="请求餐食类型")

    desc = db.Column(db.JSON, comment="内含相关追溯字段")
    
    city = db.Column(db.Text, comment="酒店所属城市")

    reason = db.Column(db.Text, comment="触发原因，默认为不可用`unavailable`")

    def __str__(self):
        return f"记录id为{self.recordid}"