from datetime import datetime

from django.db import models
from django.conf import settings
try:
    from django.contrib.auth import get_user_model
    User = settings.AUTH_USER_MODEL
except ImportError:
    from django.contrib.auth.models import User


class UserAccount(models.Model):
    """
    金教电子账户信息
    """
    user = models.ForeignKey(User, verbose_name="用户")
    username_pe = models.CharField(max_length=200, default='NULL', verbose_name="金教电子账号")
    password_pe = models.CharField(max_length=200, default='NULL', verbose_name="金教电子密码")
    status = models.CharField(max_length=50, default='0', verbose_name="账号状态")
    crawl_time = models.DateTimeField(default=datetime.now, verbose_name="爬取时间")

    class Meta:
        verbose_name = '金教电子账户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username


class UserAccountTem(models.Model):
    """
    账户临时信息
    """
    user = models.ForeignKey(User, verbose_name="用户")
    username_pe = models.CharField(max_length=200, default='NULL', verbose_name="金教电子账号")
    password_pe = models.CharField(max_length=200, default='NULL', verbose_name="金教电子密码")
    crawl_time = models.DateTimeField(default=datetime.now, verbose_name="爬取时间")

    class Meta:
        verbose_name = '账户临时信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username



class AttentanceNum(models.Model):
    """
    出勤信息
    """
    user = models.ForeignKey(User, verbose_name="用户")
    one = models.CharField(max_length=10, default='NULL', verbose_name="1-2节课")
    three = models.CharField(max_length=10, default='NULL', verbose_name="3-4节课")
    five = models.CharField(max_length=10, default='NULL', verbose_name="5-6节课")
    seven = models.CharField(max_length=10, default='NULL', verbose_name="7-8节课")
    nine = models.CharField(max_length=10, default='NULL', verbose_name="9-10节课")
    zj = models.CharField(max_length=10, default='NULL', verbose_name="增加次数")
    bk = models.CharField(max_length=10, default='NULL', verbose_name="补课次数")
    sum = models.CharField(max_length=10, default='NULL', verbose_name="本学期总次数")
    last_sum = models.CharField(max_length=10, default='NULL', verbose_name="上学期出勤次数")
    crawl_time = models.DateTimeField(default=datetime.now, verbose_name="爬取时间")

    class Meta:
        verbose_name = '出勤信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username

