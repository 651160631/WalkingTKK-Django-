#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: liyao
@license: Apache Licence 
@contact: yli@posbao.net
@site: http://www.piowind.com/
@software: PyCharm
@file: adminx.py
@time: 2017/7/4 17:04
"""
import xadmin
from .models import ElectricCharge, DormInfo_tem


class ElectricChargeAdmin(object):
    list_filter = ('crawl_time', 'user')
    list_display = ['user', "tel", "moneyLeft", "energyLeft", 'crawl_time', "message_status", "result", "crawl_status"]


class DormInfoTemAdmin(object):
    list_display = ['user', "tel", "drxiaoqu", "drlou", "drRoomId"]


xadmin.site.register(ElectricCharge, ElectricChargeAdmin)
xadmin.site.register(DormInfo_tem, DormInfoTemAdmin)

