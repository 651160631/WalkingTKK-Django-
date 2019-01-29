from datetime import datetime

from django.db import models
from django.conf import settings
try:
    from django.contrib.auth import get_user_model
    User = settings.AUTH_USER_MODEL
except ImportError:
    from django.contrib.auth.models import User


class LoginInfo(models.Model):
    """
    用户登录信息
    """
    user = models.ForeignKey(User, verbose_name="用户")
    login_time_app = models.DateTimeField(default=datetime.now, verbose_name="登录时间")
    device_type = models.CharField(max_length=200, default='NULL', verbose_name="设备类型")
    device_version = models.CharField(max_length=200, default='NULL', verbose_name="设备版本")
    app_version = models.CharField(max_length=200, default='NULL', verbose_name="app版本")
    ip = models.CharField(max_length=200, default='NULL', verbose_name="用户IP")
    imei = models.CharField(max_length=200, default='NULL', verbose_name="IMEI")
    longitude = models.CharField(max_length=200, default='NULL', verbose_name="经度")
    latitude = models.CharField(max_length=200, default='NULL', verbose_name="纬度")
    class Meta:
        verbose_name = '用户登录信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username


class TextMessage(models.Model):
    """
    短信发送内容
    """
    tel = models.CharField(max_length=11, verbose_name="电话")
    content = models.CharField(max_length=500, null=True, default="", verbose_name="短信发送内容")
    send_time = models.DateTimeField(default=datetime.now, verbose_name="短信发送时间")

    class Meta:
        verbose_name = '短信发送内容'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tel


class UserLoginStatistics(models.Model):
    """
    用户登录次数统计
    """
    login_date = models.DateField(verbose_name="统计日期", primary_key=True)
    page_view = models.IntegerField(null=False, default=0, verbose_name="登录次数")
    unique_visitor = models.IntegerField(null=False, default=0, verbose_name="独立访客")

    class Meta:
        verbose_name = '用户登录次数统计'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.login_date)


class UserRegistrationStatistics(models.Model):
    """
    用户登录次数统计
    """
    reg_date = models.DateField(verbose_name="统计日期", primary_key=True)
    people_number = models.IntegerField(null=False, default=0, verbose_name="注册人数")

    class Meta:
        verbose_name = 'APP注册人数统计'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.reg_date)

# class Suggestion(models.Model):
#     """
#     用户建议
#     """
#     user = models.ForeignKey(User, verbose_name="用户")
#     content = models.CharField(max_length=300, null=False, verbose_name="建议内容")
#     add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
#
#     class Meta:
#         verbose_name = '用户建议'
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.tel
#
# class MessageNotice(models.Model):
#     """
#     通知用户的最新消息
#     """
#     content = models.CharField(max_length=300, null=False, default="NULL", verbose_name="通知内容")  # APP通知
#     ios_version = models.CharField(max_length=100, null=True, default="NULL", verbose_name="iOS需要通知的版本")
#     andriod_version = models.CharField(max_length=100, null=True, default="NULL", verbose_name="Andriod需要通知的版本")
#     mina_version = models.CharField(max_length=100, null=True, default="NULL", verbose_name="小程序需要通知的版本")
#     grade = models.CharField(max_length=30, null=True, default="NULL", verbose_name="用户年级")  # 版本
#     add_time = models.DateTimeField(auto_now=True, null=True, verbose_name="添加时间")
#
#     class Meta:
#         verbose_name = '通知用户的最新消息'
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.tel


class VerifyCode(models.Model):
    code = models.CharField(max_length=10, verbose_name="验证码")
    tel = models.CharField(max_length=11, verbose_name="电话")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "短信验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code


class PushSettings(models.Model):
    """
    极光推送相关设置
    """
    user = models.ForeignKey(User, verbose_name="用户")
    tel = models.CharField(max_length=11, default="NULL", verbose_name="电话", help_text="和username保持一致")
    id_ios = models.CharField(max_length=200, default="NULL", null=False, verbose_name="iOS注册id")
    id_android = models.CharField(max_length=200, default="NULL", null=False, verbose_name="Android注册id")
    tag_grade = models.CharField(max_length=5, default="NULL", null=False, verbose_name="用户年级")

    class Meta:
        verbose_name = "极光推送信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username


class UserInfoDelete(models.Model):
    """
    删除用户信息
    """
    tel = models.CharField(max_length=11, default="NULL", verbose_name="电话", help_text="和username保持一致")

    class Meta:
        verbose_name = "删除用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tel
