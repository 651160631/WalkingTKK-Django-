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
from .models import UserAccount, AttentanceNum, UserAccountTem


class UserAccountAdmin(object):
    list_filter = ('crawl_time', 'user')
    list_display = ['user', 'username_pe', "password_pe", "status", "crawl_time"]


class UserAccountTemAdmin(object):
    list_filter = ('crawl_time', 'user')
    list_display = ['user', 'username_pe', "password_pe", "crawl_time"]

class AttentanceNumAdmin(object):
    list_filter = ('crawl_time', 'user')
    list_display = ["user", "one", "three", "five", "seven", "nine", "zj", "bk", "sum", "last_sum", "crawl_time"]


xadmin.site.register(UserAccount, UserAccountAdmin)
xadmin.site.register(UserAccountTem, UserAccountTemAdmin)
xadmin.site.register(AttentanceNum, AttentanceNumAdmin)


