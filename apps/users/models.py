from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

# from django.conf import settings
# try:
#     from django.contrib.auth import get_user_model
#     User = settings.AUTH_USER_MODEL
# except ImportError:
#     from django.contrib.auth.models import User


class UserProfile(AbstractUser):
    """
    用户信息
    """
    tel = models.CharField(max_length=11, verbose_name="电话",help_text="和username保持一致")
    username_jw = models.CharField(max_length=20, default='NULL', verbose_name="教务系统账号")
    password_jw = models.CharField(max_length=200, default='NULL', verbose_name="教务系统密码")
    # password_jw = models.TextField(default='NULL', verbose_name="教务系统密码")
    name = models.CharField(max_length=30,default='NULL', verbose_name="教务系统中的姓名")
    api_key = models.CharField(max_length=30, null=False, default="NULL", verbose_name="教务系统的key")  # api_key
    drxiaoqu = models.CharField(max_length=20, default='', verbose_name="宿舍园区")  # 园区编号 “31”
    drlou = models.CharField(max_length=20, default='', verbose_name="宿舍楼")  # 楼编号 “南光8”
    drRoomId = models.CharField(max_length=20, default='', verbose_name="房间编号")  # 房间编号 “0105”
    registerTime = models.DateTimeField(default=datetime.now, verbose_name="注册时间")  # 注册时间，app提供
    send_message_status = models.CharField(max_length=5, null=True, default="1", verbose_name="发送短信状态")
    isTryingReLoginJW = models.CharField(max_length=20,null=True,default="1", verbose_name="是否正在爬取信息")
    password_app = models.CharField(max_length=200, null=False, default="NULL", verbose_name="用户APP的登录密码")
    error_num_app = models.IntegerField(null=False, default=0, verbose_name="客户端登录错误次数")
    error_num_jw = models.IntegerField(null=False, default=0, verbose_name="教务系统登录错误次数")
    blacklist = models.BooleanField(default=False, verbose_name="黑名单")
    user_image_url = models.CharField(null=False, max_length=500,default="NULL", verbose_name="用户头像链接")
    week_now = models.CharField(max_length=5, default='NULL', verbose_name="当前周数，配合课程表使用,0为假期")
    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class UserInfo_tem_1(models.Model):
    """
    用户临时信息存储_1
    """
    tel = models.CharField(max_length=11, verbose_name="电话")
    username_jw = models.CharField(max_length=20, default='NULL', verbose_name="教务系统账号")
    password_jw = models.CharField(max_length=200, default='NULL', verbose_name="教务系统密码")
    drxiaoqu = models.CharField(max_length=20, default='', verbose_name="宿舍园区")
    drlou = models.CharField(max_length=20, default='', verbose_name="宿舍楼")
    drRoomId = models.CharField(max_length=20, default='', verbose_name="房间编号")

    class Meta:
        verbose_name = "用户临时信息存储_1"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tel


class UserInfo_tem_2(models.Model):
    """
    用户临时信息存储_2
    """
    tel = models.CharField(max_length=11, verbose_name="电话")
    username_jw = models.CharField(max_length=20, default='NULL', verbose_name="教务系统账号")
    password_jw = models.CharField(max_length=200, default='NULL', verbose_name="教务系统密码")
    drxiaoqu = models.CharField(max_length=20, default='', verbose_name="宿舍园区")
    drlou = models.CharField(max_length=20, default='', verbose_name="宿舍楼")
    drRoomId = models.CharField(max_length=20, default='', verbose_name="房间编号")

    class Meta:
        verbose_name = "用户临时信息存储_2"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tel


class UserInfo_tem_3(models.Model):
    """
    用户临时信息存储_3
    """
    tel = models.CharField(max_length=11, verbose_name="电话")
    username_jw = models.CharField(max_length=20, default='NULL', verbose_name="教务系统账号")
    password_jw = models.CharField(max_length=200, default='NULL', verbose_name="教务系统密码")
    drxiaoqu = models.CharField(max_length=20, default='', verbose_name="宿舍园区")
    drlou = models.CharField(max_length=20, default='', verbose_name="宿舍楼")
    drRoomId = models.CharField(max_length=20, default='', verbose_name="房间编号")

    class Meta:
        verbose_name = "用户临时信息存储_3"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tel


class UserInfo_tem_4(models.Model):
    """
    用户临时信息存储_4
    """
    tel = models.CharField(max_length=11, verbose_name="电话")
    username_jw = models.CharField(max_length=20, default='NULL', verbose_name="教务系统账号")
    password_jw = models.CharField(max_length=200, default='NULL', verbose_name="教务系统密码")
    drxiaoqu = models.CharField(max_length=20, default='', verbose_name="宿舍园区")
    drlou = models.CharField(max_length=20, default='', verbose_name="宿舍楼")
    drRoomId = models.CharField(max_length=20, default='', verbose_name="房间编号")

    class Meta:
        verbose_name = "用户临时信息存储_4"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tel
