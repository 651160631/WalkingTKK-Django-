#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: Erick

from rest_framework import serializers
from django.contrib.auth import get_user_model

from client.models import Suggestion, MessageNotice, AppLaunchImageCommon, AppLaunchImageLatest, JWMessageNotice, \
    APPMessageNotice, JWMessageGroupNotice, APPMessageGroupNotice, ErrorLog

User = get_user_model()


class SuggestionSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    image_1 = serializers.ImageField(max_length=None, allow_empty_file=False, use_url='test', help_text="图片-1")
    # image_1_base64 = serializers.CharField(allow_blank=True, help_text="图片base64码")
    image_2 = serializers.ImageField(max_length=None, allow_empty_file=False, use_url='test', help_text="图片-2")
    image_3 = serializers.ImageField(max_length=None, allow_empty_file=False, use_url='test', help_text="图片-3")
    image_4 = serializers.ImageField(max_length=None, allow_empty_file=False, use_url='test', help_text="图片-4")
    image_5 = serializers.ImageField(max_length=None, allow_empty_file=False, use_url='test', help_text="图片-5")

    class Meta:
        model = Suggestion
        fields = ('user', 'content', 'image_1', 'image_2', 'image_3', 'image_4',
                  'image_5')


class MessageNoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageNotice
        fields = '__all__'


class AppLaunchImageCommonSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppLaunchImageCommon
        fields = ('id', 'title', 'url')


class AppLaunchImageLatestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppLaunchImageLatest
        fields = ('id', 'title', 'url', 'start_date', 'end_date')


class JWMessageNoticeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = JWMessageNotice
        fields = ('id', 'user', 'read', 'content', 'add_time')


class APPMessageNoticeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = APPMessageNotice
        fields = ('id', 'user', 'title', 'read', 'content', 'add_time')


class JWMessagePushOneSerializer(serializers.ModelSerializer):
    class Meta:
        model = JWMessageNotice
        fields = ('user', 'content')


class APPMessagePushOneSerializer(serializers.ModelSerializer):
    tel = serializers.CharField(allow_blank=False, help_text="用户手机号码")
    class Meta:
        model = APPMessageNotice
        fields = ('tel', 'title', 'content')


class JWMessageGroupNoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JWMessageGroupNotice
        fields = ('content', 'all_student', 'grade')


class APPMessageGroupNoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = APPMessageGroupNotice
        fields = ('title', 'content', 'all_student', 'grade')


class JWMessageReadSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = JWMessageNotice
        fields = ('id', 'user', 'read',)


class APPMessageReadSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    msg_id = serializers.CharField(allow_blank=False, help_text="消息记录对应的id")
    class Meta:
        model = APPMessageNotice
        fields = ('id', 'user', 'msg_id', 'read')


class ErrorLogSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = ErrorLog
        fields = ('user', 'request_type', 'error')
