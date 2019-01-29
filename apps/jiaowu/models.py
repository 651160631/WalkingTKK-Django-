from datetime import datetime

from django.db import models

from django.conf import settings
try:
    from django.contrib.auth import get_user_model
    User = settings.AUTH_USER_MODEL
except ImportError:
    from django.contrib.auth.models import User


class Grade(models.Model):
    """
    用户成绩信息
    """
    user = models.ForeignKey(User, verbose_name="用户")
    stuNum = models.CharField(max_length=10, null=False, verbose_name="学生学号")
    tel = models.CharField(max_length=11, null=False, verbose_name="手机号码")
    term_id = models.CharField(max_length=20, null=True, verbose_name="学期id")
    term_name = models.CharField(max_length=50, null=True, verbose_name="学期中文名")
    sub_id = models.CharField(max_length=20, null=True, verbose_name="课程id")
    sub_name = models.CharField(max_length=100, null=True, verbose_name="课程中文名")
    credit = models.CharField(max_length=20, null=True, verbose_name="学分")
    mark = models.CharField(max_length=20, null=True, verbose_name="分数")
    method = models.CharField(max_length=20, null=True, verbose_name="修课方式")
    result = models.CharField(max_length=20, null=True, verbose_name="查询结果")
    crawl_time = models.DateTimeField(default=datetime.now, verbose_name="爬取时间")

    class Meta:
        verbose_name = "用户成绩信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tel


class TermInfo(models.Model):
    """
    用户学期信息
    """
    user = models.ForeignKey(User, verbose_name="用户")
    term_id = models.CharField(max_length=10, null=False, default="NULL",verbose_name="学期id")
    tel = models.CharField(max_length=11, null=False, verbose_name="手机号码")
    term_name = models.CharField(max_length=50, null=False, verbose_name="学期中文名")
    crawl_time = models.DateTimeField(default=datetime.now, verbose_name="爬取时间")

    class Meta:
        verbose_name = "用户学期信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tel


class Curriculum(models.Model):
    """
    用户课表信息
    """
    user = models.ForeignKey(User, verbose_name="用户")
    stuNum = models.CharField(max_length=20, null=False,default="", verbose_name="学生学号")
    tel = models.CharField(max_length=20, null=False, verbose_name="手机号码")
    xq = models.ForeignKey(TermInfo, related_name="detail", null=False, verbose_name="学期id-服务器参考")
    term_name = models.CharField(max_length=50, null=False, verbose_name="学期中文名")
    sub_id = models.CharField(max_length=20, null=True, verbose_name="课程id")
    sub_name = models.CharField(max_length=100, null=True, verbose_name="课程中文名")
    credit = models.CharField(max_length=20, null=True, verbose_name="学分")
    teacher = models.CharField(max_length=500, null=True, verbose_name="老师")
    # date_time_location = models.TextField(null=True)  # 详细信息
    start_end_week = models.CharField(max_length=50, null=True, verbose_name="起终周")
    method = models.CharField(max_length=20, null=True, verbose_name="上课方式")
    peopleNum = models.CharField(max_length=20, null=True, verbose_name="人数")
    crawl_time = models.DateTimeField(default=datetime.now, verbose_name="爬取时间")
    result = models.CharField(max_length=20, null=True, verbose_name="查询结果")
    week_day = models.CharField(max_length=50, null=True, verbose_name="周几")
    class_range = models.CharField(max_length=50, null=True, verbose_name="第几节课-第几节课")
    frequency = models.CharField(max_length=50, null=True, verbose_name="频率")
    c_classroom = models.CharField(max_length=50, null=True, verbose_name="教室")
    week_range = models.CharField(max_length=50, null=True, verbose_name="第几周-第几周")

    class Meta:
        verbose_name = "用户课表信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tel


class Attendance(models.Model):
    """
    用户出勤信息
    """
    user = models.ForeignKey(User, verbose_name="用户")
    stuNum = models.CharField(max_length=20, null=False,default="", verbose_name="学生学号")
    tel = models.CharField(max_length=20, null=False, verbose_name="手机号码")
    sub_id = models.CharField(max_length=20, null=True,default="", verbose_name="课程id")
    term_id = models.CharField(max_length=20, null=True,default="", verbose_name="学期id")
    sub_name = models.CharField(max_length=100, null=True,default="", verbose_name="课程中文名")
    teacher = models.CharField(max_length=500, null=True,default="", verbose_name="老师")
    weekId = models.CharField(max_length=20, null=True,default="", verbose_name="第几周")
    week = models.CharField(max_length=20, null=True,default="", verbose_name="星期")
    attendence_date = models.CharField(max_length=20, null=True,default="", verbose_name="缺勤日期")
    attendence_type = models.CharField(max_length=20, null=True,default="", verbose_name="类型")
    times = models.CharField(max_length=20, null=True,default="", verbose_name="次数/课时")
    result = models.CharField(max_length=20, null=True, verbose_name="查询结果")
    crawl_time = models.DateTimeField(default=datetime.now, verbose_name="爬取时间")

    class Meta:
        verbose_name = "用户出勤信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tel


class ClassSwitch(models.Model):
    """
    用户调停补课信息
    """
    user = models.ForeignKey(User, verbose_name="用户")
    stuNum = models.CharField(max_length=20, null=False,default="", verbose_name="学生学号")
    tel = models.CharField(max_length=20, null=False, verbose_name="手机号码")
    sub_id = models.CharField(max_length=20, null=True,default="", verbose_name="课程id")
    class_type = models.CharField(max_length=20, null=True,default="", verbose_name="调、停、补类型")
    sub_name = models.CharField(max_length=100, null=True,default="", verbose_name="课程中文名")
    teacher = models.CharField(max_length=500, null=True,default="", verbose_name="老师")
    date_weekId = models.CharField(max_length=20, null=True,default="", verbose_name="第几周")
    date_week = models.CharField(max_length=20, null=True,default="", verbose_name="星期")
    section = models.CharField(max_length=20, null=True,default="", verbose_name="节次")
    date_detail = models.CharField(max_length=20, null=True,default="", verbose_name="具体日期")
    classroom = models.CharField(max_length=20, null=True,default="", verbose_name="教室")
    result = models.CharField(max_length=20, null=True,default="", verbose_name="结果")
    crawl_time = models.DateTimeField(default=datetime.now, verbose_name="爬取时间")

    class Meta:
        verbose_name = "用户调停补课信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tel


class Exam(models.Model):
    """
    用户考试安排信息
    """
    user = models.ForeignKey(User, verbose_name="用户")
    stuNum = models.CharField(max_length=20, null=False,default="", verbose_name="学生学号")
    tel = models.CharField(max_length=20, null=False, verbose_name="手机号码")
    exam_id = models.CharField(max_length=20, null=True,default="", verbose_name="考试id")
    exam_name = models.CharField(max_length=50, null=True,default="", verbose_name="考试类型中文名")
    exam_date = models.CharField(max_length=50, null=True,default="", verbose_name="考试日期")
    week = models.CharField(max_length=20, null=True,default="", verbose_name="星期")
    interval = models.CharField(max_length=20, null=True,default="", verbose_name="时间段")
    exam_time = models.CharField(max_length=20, null=True,default="", verbose_name="具体时间")
    exam_location = models.CharField(max_length=20, null=True,default="", verbose_name="地点")
    exam_subject = models.CharField(max_length=20, null=True,default="", verbose_name="科目")
    method = models.CharField(max_length=20, null=True,default="", verbose_name="考核方式")
    status = models.CharField(max_length=20, null=True,default="", verbose_name="状态")
    result = models.CharField(max_length=20, null=True,default="", verbose_name="结果")
    crawl_time = models.DateTimeField(default=datetime.now, verbose_name="爬取时间")

    class Meta:
        verbose_name = "用户考试安排信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tel





