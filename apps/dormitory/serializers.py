#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: Erick

from rest_framework import serializers

from .models import ElectricCharge, DormInfo_tem


class ElectricChargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectricCharge
        fields = "__all__"


class DormInfoTemSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    drRoomId = serializers.CharField(max_length=4, min_length=4, label="宿舍编号(4位数字)", help_text="宿舍编号(4位数字)",
                                     error_messages={
                                         "min_length": "宿舍编号为4位数字！",
                                         "max_length": "宿舍编号为4位数字！"
                                     },
                                     )
    class Meta:
        model = DormInfo_tem
        fields = "__all__"


class DormInfoTemQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = DormInfo_tem
        fields = ('id', 'tel', 'drxiaoqu', 'drlou', 'drRoomId', 'user_id')
