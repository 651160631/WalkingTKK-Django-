#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: Erick
import re
from datetime import datetime, timedelta

from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from rest_framework.response import Response
from rest_framework import status

from user_operation.models import VerifyCode
from apps.users.models import UserInfo_tem_1, UserInfo_tem_2, UserInfo_tem_3, UserInfo_tem_4

User = get_user_model()

# 手机号码正则表达式
REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^17\d{9}$"


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11, help_text="手机号码")

    def validate_mobile(self, mobile):
        """
        验证手机号码
        :param data:
        :return:
        """
        # 手机是否被注册
        # if User.objects.filter(tel=mobile).count():
        #     mobile_msg = {
        #         "result": "该手机号码已注册"
        #     }
        #     raise serializers.ValidationError(mobile_msg)

        # 验证手机号码时候合法
        if not re.match(REGEX_MOBILE, mobile):
            mobile_msg = {
                "result": "手机号码格式错误"
            }
            raise serializers.ValidationError(mobile_msg)

        # 验证发送频率
        two_minite_ago = datetime.now() - timedelta(hours=0, minutes=2, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=two_minite_ago, tel=mobile).count():
            mobile_msg = {
                "result": "距离上次发送未超过2分钟"
            }
            raise serializers.ValidationError(mobile_msg)
        return mobile


class UserRegSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=4, write_only=True, min_length=4, label="验证码",
                                 error_messages={
                                     "blank": "请输入验证码",
                                     "required": "请输入验证码",
                                     "min_length": "验证码格式错误",
                                     "max_length": "验证码格式错误"
                                     },
                                 help_text="验证码")
    #
    username = serializers.CharField(required=True, allow_blank=False, label="用户名",
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已存在")],
                                     help_text="用户名，与手机号码一致"
                                     )

    password = serializers.CharField(
        style={"input_type": "password"}, label="密码", write_only=True, min_length=8, max_length=32, help_text="密码",
    )

    def create(self, validated_data):
        user = super(UserRegSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    # def validate_code(self, code):
    #     verify_records = VerifyCode.objects.filter(tel=self.initial_data["username"]).order_by("-add_time")
    #     if verify_records:
    #         last_record = verify_records[0]
    #         five_minutes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
    #         if five_minutes_ago > last_record.add_time:
    #             code_msg = {
    #                 "result": "验证码已过期"
    #             }
    #             # return Response(code_msg, status=status.HTTP_400_BAD_REQUEST)
    #             raise serializers.ValidationError(code_msg)
    #         if last_record.code != code:
    #             code_msg = {
    #                 "result": "验证码错误，请核实"
    #             }
    #             # return Response(code_msg, status=status.HTTP_400_BAD_REQUEST)
    #             raise serializers.ValidationError(code_msg)
    #     else:
    #         code_msg = {
    #             "result": "验证码错误，请核实"
    #         }
    #         # return Response(code_msg, status=status.HTTP_400_BAD_REQUEST)
    #         raise serializers.ValidationError(code_msg)

    def validate(self, attrs):
        # 验证完之后将code删除
        # attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ("username", "tel", "code", "password")


class TelInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("tel",)


class PasswordChangeWithKnowRawSerializer(serializers.ModelSerializer):
    passwordNew = serializers.CharField(max_length=32, min_length=8, required=True, allow_blank=False, label="用户新密码",
                                        error_messages={
                                            "required": "请输入新密码",
                                            "min_length": "新密码最短为8位",
                                            "max_length": "新密码最长为32位"
                                        },
                                        help_text="用户新密码"
                                        )
    class Meta:
        model = User
        fields = ("username", "tel", "password", "passwordNew")


class PasswordChangeWithSmsSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=4, write_only=True, min_length=4, label="验证码",
                                 error_messages={
                                     "blank": "请输入验证码",
                                     "required": "请输入验证码",
                                     "min_length" : "验证码格式错误",
                                     "max_length": "验证码格式错误"
                                     },
                                 help_text="验证码")

    username = serializers.CharField(required=True, allow_blank=False, label="用户名")

    passwordNew = serializers.CharField(max_length=32, min_length=8, required=True, allow_blank=False, label="用户新密码",
                                        error_messages={
                                            "required": "请输入新密码",
                                            "min_length": "新密码最短为8位",
                                            "max_length": "新密码最长为32位"
                                        },
                                        help_text="用户新密码"
                                        )

    def create(self, validated_data):
        user = super(PasswordChangeWithSmsSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data["passwordNew"])
        user.save()
        return user

    def validate_code(self, code):
        verify_records = VerifyCode.objects.filter(tel=self.initial_data["username"]).order_by("-add_time")
        if verify_records:
            last_record = verify_records[0]
            five_minutes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_minutes_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")
            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")
        else:
            raise serializers.ValidationError("验证码错误")

    def validate(self, attrs):
        # 验证完之后将code删除
        # attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ("username", "tel", "code", "passwordNew")


class SmsSwitchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("send_message_status",)


class LoginErrorNumSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ()


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "tel", "username_jw", "name", "api_key", "drxiaoqu", "drlou", "drRoomId", "week_now",
                  "isTryingReLoginJW", "send_message_status")


class UserJwBindSerializer(serializers.ModelSerializer):
    username_jw = serializers.CharField(max_length=20, allow_blank=False, label="教务系统账号")
    password_jw = serializers.CharField(max_length=200, allow_blank=False, label="教务系统密码")
    drxiaoqu = serializers.CharField(max_length=20, allow_blank=False, label="宿舍园区")
    drlou = serializers.CharField(max_length=20, allow_blank=False, label="宿舍楼")
    drRoomId = serializers.CharField(max_length=4, min_length=4, label="宿舍编号(4位数字)", help_text="宿舍编号(4位数字)",
                                     error_messages={
                                         "min_length": "宿舍编号为4位数字！",
                                         "max_length": "宿舍编号为4位数字！"
                                     },
                                     )
    class Meta:
        model = User
        fields = ( "username_jw", "password_jw", "drxiaoqu", "drlou", "drRoomId")


class UserInfoTem1Serializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo_tem_1
        fields = '__all__'


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('tel', 'password')


class UserImageSerializer(serializers.ModelSerializer):
    id = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    user_image_base64 = serializers.CharField(allow_blank=True, help_text="用户头像图片base64码")

    class Meta:
        model = User
        fields = ('id', 'user_image_base64')


class UserinfoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'tel', 'username_jw', 'password_jw', 'name', 'api_key', 'drxiaoqu', 'drlou', 'drRoomId',
                  'send_message_status')


class UserLoginInfoCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("tel",)


class CurrentWeekSerializer(serializers.ModelSerializer):
    id = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = User
        fields = ('id', 'week_now')


class AddUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, allow_blank=False, label="用户名",
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已存在")],
                                     help_text="用户名，与手机号码一致"
                                     )

    password = serializers.CharField(
        style={"input_type": "password"}, label="密码", write_only=True, min_length=8, max_length=32, help_text="密码",
    )

    def create(self, validated_data):
        user = super(AddUserSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    class Meta:
        model = User
        fields = ("username", "tel", "password", 'drxiaoqu', 'drlou', 'drRoomId','username_jw', 'password_jw')
