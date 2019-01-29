#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: Erick
from datetime import datetime, timedelta

from rest_framework import serializers
from django.contrib.auth import get_user_model

from user_operation.models import PushSettings, UserInfoDelete, LoginInfo

User = get_user_model()


class PushSettingsSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    id_ios = serializers.CharField(max_length=200, allow_blank=True, help_text="ios设备注册id")
    id_android = serializers.CharField(max_length=200, allow_blank=True, help_text="Android设备注册id")

    class Meta:
        model = PushSettings
        fields = ('user', 'id_ios', 'id_android')


class PushSettingsQuerySerializer(serializers.ModelSerializer):

    class Meta:
        model = PushSettings
        fields = "__all__"


class UserInfoDeleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserInfoDelete
        fields = ('tel',)


class UserLoginInfoSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = LoginInfo
        fields = ('user', "device_type", "ip", "imei", "device_version", "app_version","latitude", "longitude")


class UpdateStatisticsSerializer(serializers.ModelSerializer):
    info = serializers.CharField(max_length=50, allow_blank=False, help_text="更新统计信息")

    class Meta:
        model = PushSettings
        fields = ('info', )
