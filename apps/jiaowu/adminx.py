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
from .models import Grade, TermInfo, Curriculum, Attendance, ClassSwitch, Exam


class GradeAdmin(object):
    list_filter = ('crawl_time', 'user')
    list_display = ['user', 'stuNum', "tel", 'term_id', "term_name",'sub_id', "sub_name", 'credit', 'mark', "method",
                    "result", 'crawl_time']


class TermInfoAdmin(object):
    list_filter = ('crawl_time', 'tel')
    list_display = ['tel', "term_id", 'term_name', 'crawl_time']


class CurriculumAdmin(object):
    list_filter = ('crawl_time', 'user')
    list_display = ['user', 'stuNum', "tel", 'xq', "term_name",'sub_id', "sub_name", 'credit', 'teacher',
                    "start_end_week", "method", 'peopleNum', "week_day", 'class_range',
                    "frequency",'c_classroom', "week_range", 'crawl_time', 'result']


class AttendanceAdmin(object):
    list_filter = ('crawl_time', 'user')
    list_display = ['user', 'stuNum', "tel", "sub_id", 'term_id', "sub_name", 'sub_id', "sub_name", 'teacher', 'weekId',
                    "week", "attendence_date", 'attendence_type', "times", "result", 'crawl_time']


class ClassSwitchAdmin(object):
    list_filter = ('crawl_time', 'user')
    list_display = ['user', 'stuNum', "tel", "sub_id", 'class_type', "teacher", 'date_weekId', "date_week", 'section',
                    'date_detail', "classroom", "result", 'crawl_time']


class ExamAdmin(object):
    list_filter = ('crawl_time', 'user')
    list_display = ['user', 'stuNum', "tel", "exam_id", 'exam_name', "exam_date", 'week', "interval", 'exam_location',
                    'exam_subject', "method", "status","result", 'crawl_time']


xadmin.site.register(Grade, GradeAdmin)
xadmin.site.register(TermInfo, TermInfoAdmin)
xadmin.site.register(Curriculum, CurriculumAdmin)
xadmin.site.register(Attendance, AttendanceAdmin)
xadmin.site.register(ClassSwitch, ClassSwitchAdmin)
xadmin.site.register(Exam, ExamAdmin)
