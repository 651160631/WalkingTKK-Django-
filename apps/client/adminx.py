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
from .models import Suggestion, MessageNotice, AppLaunchImageCommon, AppLaunchImageLatest, JWMessageNotice, \
    JWMessageGroupNotice, APPMessageNotice, APPMessageGroupNotice, ErrorLog


class SuggestionAdmin(object):
    list_display = ['user', 'content', "add_time"]


class MessageNoticeAdmin(object):
    list_display = ["content", "ios_version", "andriod_version", "mina_version", "grade", "add_time"]


class AppLaunchImageCommonAdmin(object):
    list_display = ['title', 'url', 'platform', 'size', "add_time"]


class AppLaunchImageLatestAdmin(object):
    list_display = ['title', 'url', 'platform', 'size', "start_date", "end_date", "add_time"]


class JWMessageNoticeAdmin(object):
    list_display = ['user', 'content', 'read', "add_time"]


class JWMessageGroupNoticeAdmin(object):
    list_display = ['content', 'all_student', "grade", "add_time"]


class APPMessageNoticeAdmin(object):
    list_display = ['user', 'title', 'content', 'read', "add_time"]


class APPMessageGroupNoticeAdmin(object):
    list_display = ['title', 'content', 'all_student', "grade", "add_time"]


class ErrorLogAdmin(object):
    list_filter = ("add_time", )
    list_display = ['user', 'request_type', 'error', "add_time"]


xadmin.site.register(MessageNotice, MessageNoticeAdmin)
xadmin.site.register(Suggestion, SuggestionAdmin)
xadmin.site.register(AppLaunchImageCommon, AppLaunchImageCommonAdmin)
xadmin.site.register(AppLaunchImageLatest, AppLaunchImageLatestAdmin)
xadmin.site.register(JWMessageNotice, JWMessageNoticeAdmin)
xadmin.site.register(JWMessageGroupNotice, JWMessageGroupNoticeAdmin)
xadmin.site.register(APPMessageNotice, APPMessageNoticeAdmin)
xadmin.site.register(APPMessageGroupNotice, APPMessageGroupNoticeAdmin)
xadmin.site.register(ErrorLog, ErrorLogAdmin)



