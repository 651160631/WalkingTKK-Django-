from datetime import datetime

from django.db import models

from django.conf import settings
try:
    from django.contrib.auth import get_user_model
    User = settings.AUTH_USER_MODEL
except ImportError:
    from django.contrib.auth.models import User

from utils.uoload_file_alioss import UploadImageOssStorage

# Create your models here.

class Suggestion(models.Model):
    """
    用户建议
    """
    user = models.ForeignKey(User, verbose_name="用户")
    content = models.CharField(max_length=300, null=False, verbose_name="建议内容")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    image_1_url = models.CharField(max_length=500, null=False, default="NULL", verbose_name="用户截图-1")
    image_2_url = models.CharField(max_length=500, null=False, default="NULL", verbose_name="用户截图-2")
    image_3_url = models.CharField(max_length=500, null=False, default="NULL", verbose_name="用户截图-3")
    image_4_url = models.CharField(max_length=500, null=False, default="NULL", verbose_name="用户截图-4")
    image_5_url = models.CharField(max_length=500, null=False, default="NULL", verbose_name="用户截图-5")
    class Meta:
        verbose_name = '用户建议'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username

class MessageNotice(models.Model):
    """
    通知用户的最新消息
    """
    title = models.CharField(max_length=100, null=False, default="NULL", verbose_name="通知标题")
    content = models.CharField(max_length=300, null=False, default="NULL", verbose_name="通知内容")
    ios_version = models.CharField(max_length=100, null=True, default="NULL", verbose_name="iOS需要通知的版本")
    andriod_version = models.CharField(max_length=100, null=True, default="NULL", verbose_name="Andriod需要通知的版本")
    mina_version = models.CharField(max_length=100, null=True, default="NULL", verbose_name="小程序需要通知的版本")
    grade = models.CharField(max_length=30, null=True, default="NULL", verbose_name="用户年级")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '通知用户的最新消息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

class AppLaunchImageCommon(models.Model):
    """
    APP 启动页图片 - 日常
    """
    PLATFORM_CHOICES = (
        ('iOS', 'iOS'),
        ('Android', 'Android')
    )
    SIZE_CHOICES = (
        ('640', '640'),
        ('750', '750'),
        ('1242', '1242'),
        ('1125', '1125')
    )
    title = models.CharField(max_length=200, null=False, default="NULL", verbose_name="图片标题")
    url = models.CharField(max_length=500, null=False, default="", verbose_name="图片链接")
    platform = models.CharField(max_length=20, null=False, choices=PLATFORM_CHOICES, default="iOS", verbose_name="使用平台")
    size = models.CharField(max_length=20, null=False, choices=SIZE_CHOICES, default="640", verbose_name="图片的宽度")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = 'APP启动页图片 - 日常'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

class AppLaunchImageLatest(models.Model):
    """
    APP 启动页图片 - 最新
    """
    PLATFORM_CHOICES = (
        ('iOS', 'iOS'),
        ('Android', 'Android')
    )
    SIZE_CHOICES = (
        ('640', '640'),
        ('750', '750'),
        ('1242', '1242'),
        ('1125', '1125')
    )
    title = models.CharField(max_length=200, null=False, default="NULL", verbose_name="图片标题")
    url = models.CharField(max_length=500, null=False, default="", verbose_name="图片链接")
    platform = models.CharField(max_length=20, null=False, choices=PLATFORM_CHOICES, default="iOS", verbose_name="使用平台")
    size = models.CharField(max_length=20, null=False, choices=SIZE_CHOICES, default="640", verbose_name="图片的宽度")
    start_date = models.DateTimeField(null=False, verbose_name="开始展示日期")
    end_date = models.DateTimeField(null=False, verbose_name="结束展示日期")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = 'APP启动页图片 - 最新'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class JWMessageNotice(models.Model):
    """
    通知用户关于教务系统的消息
    """
    user = models.ForeignKey(User, verbose_name="用户")
    content = models.CharField(max_length=300, null=False, default="NULL", verbose_name="通知内容")
    read = models.BooleanField(default=False, null=False, verbose_name="是否已读")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '通知用户关于教务系统的消息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content


class APPMessageNotice(models.Model):
    """
    通知用户关于APP的消息
    """
    user = models.ForeignKey(User, verbose_name="用户")
    title = models.CharField(max_length=100, null=False, default="NULL", verbose_name="通知标题")
    content = models.CharField(max_length=300, null=False, default="NULL", verbose_name="通知内容")
    read = models.BooleanField(default=False, null=False, verbose_name="是否已读")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '通知用户关于APP的消息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class JWMessageGroupNotice(models.Model):
    """
    群发教务系统的消息记录
    """
    content = models.CharField(max_length=300, null=False, default="NULL", verbose_name="通知内容")
    all_student = models.BooleanField(default=False, verbose_name="通知所有人", help_text="若勾选，则用户年级填写NULL")
    grade = models.CharField(max_length=30, null=True, default="NULL", verbose_name="用户年级", help_text="一次填写一个年级，如 2015")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '群发教务系统的消息记录'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content


class APPMessageGroupNotice(models.Model):
    """
    群发关于APP的消息记录
    """
    title = models.CharField(max_length=100, null=False, default="NULL", verbose_name="通知标题")
    content = models.CharField(max_length=300, null=False, default="NULL", verbose_name="通知内容")
    all_student = models.BooleanField(default=False, verbose_name="通知所有人", help_text="若勾选，则用户年级填写NULL")
    grade = models.CharField(max_length=30, null=True, default="NULL", verbose_name="用户年级", help_text="一次填写一个年级，如 2015")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '群发关于APP的消息记录'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class ErrorLog(models.Model):
    """
    客户端Bug记录
    """
    user = models.ForeignKey(User, verbose_name="用户")
    request_type = models.CharField(max_length=200, null=False, default="NULL", verbose_name="请求类型")
    error = models.CharField(max_length=500, null=True, default="NULL", verbose_name="错误内容")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '客户端Bug记录'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.request_type
