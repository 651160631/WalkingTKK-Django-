#!/usr/bin/env python3
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
# from extra_apps import xadmin
from .models import LoginInfo, TextMessage, VerifyCode, PushSettings, UserInfoDelete, UserLoginStatistics, \
    UserRegistrationStatistics

from django.db.models import Count

from django.contrib.auth import get_user_model
User = get_user_model()



class LoginInfoAdmin(object):
    list_filter = ('login_time_app', 'user',"device_type", "ip", "imei", "device_version", "app_version")
    list_display = ['user', 'login_time_app', "device_type", "ip", "imei", "device_version", "app_version", "latitude", "longitude"]


class TextMessageAdmin(object):
    list_display = ["tel", "content", "send_time"]


class VerifyCodeAdmin(object):
    list_display = ['code', 'tel', "add_time"]


class PushSettingsAdmin(object):
    list_display = ['user', 'id_ios', "id_android", "tag_grade"]


class UserInfoDeleteAdmin(object):
    list_display = ['tel']


# class UserLoginStatisticsAdmin(object):
#     login_nums = LoginInfo.objects.extra({'login_time_app': "date(login_time_app)"}).values('login_time_app').annotate(number=Count('id'))
#     people_nums = LoginInfo.objects.extra({'login_time_app': "date(login_time_app)"}).values('login_time_app').annotate(p_number=Count('user_id',distinct=True))
#     for login_num in login_nums:
#         login_date = login_num["login_time_app"]
#         login_people_num = login_num["number"]
#         user_login = UserLoginStatistics(login_date=login_date, page_view=login_people_num)
#         user_login.save()
#     for people_num in people_nums:
#         login_date = people_num["login_time_app"]
#         p_number = people_num["p_number"]
#         UserLoginStatistics.objects.filter(login_date=login_date).update(unique_visitor=p_number)
#     data_charts = {
#         "user_login_info": {'title': "用户登录次数统计", "x-field": "login_date", "y-field": ("page_view", "unique_visitor")},
#     }
#     list_display = ['login_date', 'page_view', 'unique_visitor']
#
#
# class UserRegistrationStatisticsAdmin(object):
#     reg_nums = User.objects.extra({'registerTime': "date(registerTime)"}).values('registerTime').annotate(number=Count('id'))
#     for reg in reg_nums:
#         registerTime = reg["registerTime"]
#         reg_num = reg["number"]
#         user_login = UserRegistrationStatistics(reg_date=registerTime, people_number=reg_num)
#         user_login.save()
#     data_charts = {
#         "user_reg_info": {'title': "APP注册人数统计", "x-field": "reg_date", "y-field": "people_number"},
#     }
#     list_display = ['reg_date', 'people_number']


xadmin.site.register(VerifyCode, VerifyCodeAdmin)
xadmin.site.register(LoginInfo, LoginInfoAdmin)
xadmin.site.register(TextMessage, TextMessageAdmin)
xadmin.site.register(PushSettings, PushSettingsAdmin)
xadmin.site.register(UserInfoDelete, UserInfoDeleteAdmin)
# xadmin.site.register(UserLoginStatistics, UserLoginStatisticsAdmin)
# xadmin.site.register(UserRegistrationStatistics, UserRegistrationStatisticsAdmin)


