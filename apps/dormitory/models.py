from datetime import datetime

from django.db import models
from django.conf import settings
try:
    from django.contrib.auth import get_user_model
    User = settings.AUTH_USER_MODEL
except ImportError:
    from django.contrib.auth.models import User


class ElectricCharge(models.Model):
    """
    用户宿舍电费信息
    """
    user = models.ForeignKey(User, verbose_name="用户")
    tel = models.CharField(max_length=20, null=False, verbose_name="手机号码", help_text="手机号码")
    moneyLeft = models.CharField(max_length=20, null=False, verbose_name="剩余电费")
    energyLeft = models.CharField(max_length=20, null=False, verbose_name="剩余电量")
    crawl_time = models.DateTimeField(default=datetime.now, verbose_name="爬取时间")
    message_status = models.CharField(max_length=5,null=True,default="1", verbose_name="发送短信状态")
    result = models.CharField(max_length=5,null=True,default="1", verbose_name="爬取结果")
    crawl_status = models.CharField(max_length=5,null=True,default="0", verbose_name="爬取信息状态")  # 0代表爬取成功，1代表正在爬取

    class Meta:
        verbose_name = "用户宿舍电费信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tel


class DormInfo_tem(models.Model):
    """
    用户宿舍信息临时存储
    """
    user = models.ForeignKey(User, verbose_name="用户")
    tel = models.CharField(max_length=20, null=False, verbose_name="手机号码", help_text="手机号码")
    drxiaoqu = models.CharField(max_length=20, null=False, verbose_name="宿舍园区", help_text="宿舍园区，如 31")
    drlou = models.CharField(max_length=20, null=False, verbose_name="宿舍楼", help_text="宿舍楼，如 南光8")
    drRoomId = models.CharField(max_length=20, null=False, verbose_name="房间编号", help_text="房间编号，如 0105")

    class Meta:
        verbose_name = "用户宿舍信息临时存储"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tel
