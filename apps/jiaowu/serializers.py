#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: Erick
from rest_framework import serializers

from .models import Grade, TermInfo, Curriculum, Attendance, ClassSwitch, Exam


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = "__all__"


class CurriculumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curriculum
        fields = "__all__"


class TermInfoSerializer(serializers.ModelSerializer):
    detail = CurriculumSerializer(many=True)
    class Meta:
        model = TermInfo
        fields = ('term_id','term_name','detail',)


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = "__all__"


class ClassSwitchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassSwitch
        fields = "__all__"


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = "__all__"


