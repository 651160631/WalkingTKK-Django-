#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: Erick
from datetime import datetime, timedelta

from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import UserAccountTem, UserAccount, AttentanceNum

User = get_user_model()


class AccountTemSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    crawl_time = serializers.HiddenField(
        default=datetime.now
    )
    username_pe = serializers.CharField(max_length=200,  allow_blank=False, help_text="金教电子账号")
    password_pe = serializers.CharField(max_length=200,  allow_blank=False, help_text="金教电子密码")
    class Meta:
        model = UserAccountTem
        fields = "__all__"


class AccountTemServerSerializer(serializers.ModelSerializer):
    crawl_time = serializers.HiddenField(
        default=datetime.now
    )
    username_pe = serializers.CharField(max_length=200,  allow_blank=False, help_text="金教电子账号")
    password_pe = serializers.CharField(max_length=200,  allow_blank=False, help_text="金教电子密码")
    class Meta:
        model = UserAccountTem
        fields = "__all__"


class AccountSerializer(serializers.ModelSerializer):
    crawl_time = serializers.HiddenField(
        default=datetime.now
    )
    class Meta:
        model = UserAccount
        fields = "__all__"


class AttentanceNumSerializer(serializers.ModelSerializer):
    crawl_time = serializers.HiddenField(
        default=datetime.now
    )
    class Meta:
        model = AttentanceNum
        fields = "__all__"


class DeleteAccountTemSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccountTem
        fields = ('id',)






