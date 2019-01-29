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
from xadmin import views

from .models import UserInfo_tem_1,UserInfo_tem_2,UserInfo_tem_3,UserInfo_tem_4


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "walkingTKK Administration"
    site_footer = "Developed by ZHU Zean. Based on Xadmin"
    # menu_style = "accordion"


class UserInfoTemAdmin(object):
    list_display = ['tel', 'username_jw', "password_jw", 'drxiaoqu', 'drlou', "drRoomId"]


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(UserInfo_tem_1, UserInfoTemAdmin)
xadmin.site.register(UserInfo_tem_2, UserInfoTemAdmin)
xadmin.site.register(UserInfo_tem_3, UserInfoTemAdmin)
xadmin.site.register(UserInfo_tem_4, UserInfoTemAdmin)
