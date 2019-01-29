from random import choice
import base64
import os
import re
from datetime import datetime, timedelta

from django.shortcuts import render
from django.contrib.auth import authenticate

from django.contrib.auth import get_user_model

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework import status
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination


from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


from .serializers import SmsSerializer, UserRegSerializer, TelInfoSerializer, PasswordChangeWithKnowRawSerializer, \
    PasswordChangeWithSmsSerializer, SmsSwitchSerializer, LoginErrorNumSerializer, UserDetailSerializer, \
    UserJwBindSerializer, LoginSerializer, UserImageSerializer, UserinfoUpdateSerializer, UserInfoTem1Serializer, \
    UserLoginInfoCheckSerializer, CurrentWeekSerializer, AddUserSerializer
from apps.users.models import UserProfile, UserInfo_tem_1, UserInfo_tem_2, UserInfo_tem_3, UserInfo_tem_4
from user_operation.models import VerifyCode
from client.models import JWMessageNotice, APPMessageNotice

from utils import aliyun_text_message
from utils.permissions import IsOwnerOrReadOnly
from utils.deal_password import Prpcrypt
from utils.uoload_file_alioss import UploadImageOssStorage

User = get_user_model()
pc = Prpcrypt()

# Create your views here.

class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(tel=username))
            if user.check_password(password):
                return user
        except Exception as e:
            print(e)
            return None


class SmsCodeViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码/Basic Auth
    """

    serializer_class = SmsSerializer
    authentication_classes = (BasicAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def generate_code(self):
        """
        生成四位数的验证码
        :return:
        """
        seeds = "0123456789"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))
        return "".join(random_str)

    def validate_mobile(self, mobile):
        """
        验证手机号码
        :param data:
        :return:
        """
        # 手机号码正则表达式
        REGEX_MOBILE = "^1[3578]\d{9}$|^147\d{8}$|^17\d{9}$"

        # 手机是否被注册
        # if User.objects.filter(tel=mobile).count():
        #     mobile_msg = {
        #         "result": "该手机号码已注册"
        #     }
        #     raise serializers.ValidationError(mobile_msg)

        # 验证手机号码时候合法
        if not re.match(REGEX_MOBILE, mobile):
            mobile_msg = {
                "result": "手机号码格式错误，目前只支持中国大陆手机号码。"
            }
            return mobile_msg

        # 验证发送频率
        two_minite_ago = datetime.now() - timedelta(hours=0, minutes=2, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=two_minite_ago, tel=mobile).count():
            mobile_msg = {
                "result": "发送短信过于频繁，请耐心等待哦~"
            }
            return mobile_msg
        return None


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        mobile = request.data.get("mobile")
        validate_result = self.validate_mobile(mobile=mobile)
        if validate_result:
            return Response(validate_result, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.is_valid(raise_exception=True)
            # mobile = serializer.validated_data["mobile"]
            code = self.generate_code()
            content = {"code": code}
            aliyun = aliyun_text_message.Aliyun()
            sms_status = aliyun.send_sms(mobile, repr(content), "行走嘉园", "SMS_69205776")
            if not sms_status["success"]:
                sms_msg = {
                    "result": "未能发送验证码短信，如持续出现该情况，请与我们联系contact@forsource.cn"
                }
                return Response(sms_msg, status=status.HTTP_400_BAD_REQUEST)
            else:
                code_record = VerifyCode(code=code, tel=mobile)
                code_record.save()
                sms_msg = {
                    "result": "验证码已发送~"
                }
                return Response(sms_msg, status=status.HTTP_200_OK)


class UserRegViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    用户注册/Basic Auth
    """
    serializer_class = UserRegSerializer
    queryset = User.objects.all()
    authentication_classes = (BasicAuthentication, SessionAuthentication)

    def validate_code(self, code,tel):
        verify_records = VerifyCode.objects.filter(tel=tel).order_by("-add_time")
        if verify_records:
            last_record = verify_records[0]
            five_minutes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_minutes_ago > last_record.add_time:
                code_msg = {
                    "result": "验证码已过期"
                }
                return code_msg
                # raise serializers.ValidationError(code_msg)
            if last_record.code != code:
                code_msg = {
                    "result": "验证码错误，请核实"
                }
                return code_msg
                # raise serializers.ValidationError(code_msg)
            else:
                return None
        else:
            code_msg = {
                "result": "验证码错误，请核实"
            }
            return code_msg
            # raise serializers.ValidationError(code_msg)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        username = request.data.get("username")
        tel = request.data.get("tel")
        password = request.data.get("password")
        code = request.data.get("code")
        if username != tel:
            fail_msg = {
                "result": "username与tel不一致，请前端开发人员注意(微笑脸)"
            }
            return Response(fail_msg, status=status.HTTP_400_BAD_REQUEST)
        elif UserProfile.objects.filter(username=username):
            fail_msg = {
                "result": "该账号已注册，快去登录吧。"
            }
            return Response(fail_msg, status=status.HTTP_400_BAD_REQUEST)
        elif len(username) == 0 or len(password) == 0 or len(code) == 0 or len(tel) == 0:
            fail_msg = {
                "result": "请填写所有内容！"
            }
            return Response(fail_msg, status=status.HTTP_400_BAD_REQUEST)
        elif len(username) != 11 or len(tel) != 11:
            fail_msg = {
                "result": "请填写正确的手机号码，暂时只支持中国大陆手机号码哦！"
            }
            return Response(fail_msg, status=status.HTTP_400_BAD_REQUEST)
        elif len(code) != 4:
            fail_msg = {
                "result": "验证码为4位数字哦！"
            }
            return Response(fail_msg, status=status.HTTP_400_BAD_REQUEST)
        elif self.validate_code(code, tel):
            code_msg = self.validate_code(code, tel)
            return Response(code_msg, status=status.HTTP_400_BAD_REQUEST)
        elif len(password) < 8 or len(password) > 32:
            fail_msg = {
                "result": "密码长度不能小于8位或大于32位哦~"
            }
            return Response(fail_msg, status=status.HTTP_400_BAD_REQUEST)

        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        # 将用户的密码以密文形式备份
        password_app = pc.encrypt(password)
        UserProfile.objects.filter(tel=tel).update(password_app=password_app)
        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username
        headers = self.get_success_headers(serializer.data)
        success_msg = {
            "result": "注册成功！赶快去登录吧 ^_^"
        }
        return Response(success_msg, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()


class TelInfoViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    验证用户手机号码是否存在/Basic Auth
    """
    serializer_class = TelInfoSerializer
    authentication_classes = (BasicAuthentication, SessionAuthentication)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tel = serializer.validated_data["tel"]
        tel_record = User.objects.filter(tel=tel).count()
        if tel_record:
            tel_msg = {
                "result": "手机号码已存在"
            }
            return Response(tel_msg, status=status.HTTP_400_BAD_REQUEST)
        else:
            tel_msg = {
                "result": "手机号码不存在"
            }
            return Response(tel_msg, status=status.HTTP_200_OK)


class PasswordChangeWithKnowRawViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    修改用户密码(已知原密码)/Basic Auth
    """
    serializer_class = PasswordChangeWithKnowRawSerializer
    authentication_classes = (BasicAuthentication, SessionAuthentication)

    def create(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        passwordNew = request.data.get("passwordNew")
        user = authenticate(username=username, password=password)
        if user:
            u = User.objects.get(username__exact=username)
            u.set_password(passwordNew)
            u.save()
            # 将用户的密码备份
            password_app = pc.encrypt(passwordNew)
            UserProfile.objects.filter(username=username).update(password_app=password_app)
            password_change_msg = {
                "result": "密码已修改成功"
            }
            return Response(password_change_msg, status=status.HTTP_200_OK)
        else:
            password_change_msg = {
                "result": "原密码不正确"
            }
            return Response(password_change_msg, status=status.HTTP_400_BAD_REQUEST)


class PasswordChangeWithSmsViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    修改用户密码(忘记原密码，通过短信验证码修改)/Basic Auth
    """
    serializer_class = PasswordChangeWithSmsSerializer
    authentication_classes = (BasicAuthentication, SessionAuthentication)

    def validate_code(self, code,tel):
        verify_records = VerifyCode.objects.filter(tel=tel).order_by("-add_time")
        if verify_records:
            last_record = verify_records[0]
            five_minutes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_minutes_ago > last_record.add_time:
                code_msg = {
                    "result": "验证码已过期"
                }
                return code_msg
                # raise serializers.ValidationError(code_msg)
            if last_record.code != code:
                code_msg = {
                    "result": "验证码错误，请核实"
                }
                return code_msg
                # raise serializers.ValidationError(code_msg)
            else:
                return None
        else:
            code_msg = {
                "result": "验证码错误，请核实"
            }
            return code_msg
            # raise serializers.ValidationError(code_msg)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        username = request.data.get("username")
        tel = request.data.get("tel")
        passwordNew = request.data.get("passwordNew")
        code = request.data.get("code")
        if username != tel:
            fail_msg = {
                "result": "username与tel不一致，请前端开发人员注意(微笑脸)"
            }
            return Response(fail_msg, status=status.HTTP_400_BAD_REQUEST)
        elif len(username) == 0 or len(passwordNew) == 0 or len(code) == 0 or len(tel) == 0:
            fail_msg = {
                "result": "请填写所有内容！"
            }
            return Response(fail_msg, status=status.HTTP_400_BAD_REQUEST)
        elif len(username) != 11 or len(tel) != 11:
            fail_msg = {
                "result": "请填写正确的手机号码，暂时只支持中国大陆手机号码哦！"
            }
            return Response(fail_msg, status=status.HTTP_400_BAD_REQUEST)
        elif len(code) != 4:
            fail_msg = {
                "result": "验证码为4位数字哦~"
            }
            return Response(fail_msg, status=status.HTTP_400_BAD_REQUEST)
        elif self.validate_code(code, tel):
            code_msg = self.validate_code(code, tel)
            return Response(code_msg, status=status.HTTP_400_BAD_REQUEST)
        elif len(passwordNew) < 8 or len(passwordNew) > 32:
            fail_msg = {
                "result": "密码长度不能小于8位或大于32位哦~"
            }
            return Response(fail_msg, status=status.HTTP_400_BAD_REQUEST)
        serializer.is_valid(raise_exception=True)
        username = request.data.get("username")
        passwordNew = request.data.get("passwordNew")
        u = User.objects.get(username__exact=username)
        u.set_password(passwordNew)
        u.save()
        password_app = pc.encrypt(passwordNew)
        UserProfile.objects.filter(username=username).update(password_app=password_app)
        password_change_msg = {
            "result": "密码已修改成功!"
        }
        return Response(password_change_msg, status=status.HTTP_200_OK)


class SmsSwitchViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    短信发送开关，"1"开启短信通知，"0"关闭短信通知
    """
    serializer_class = SmsSwitchSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsOwnerOrReadOnly,IsAuthenticated)

    def create(self, request, *args, **kwargs):
        try:
            send_message_status = request.data.get("send_message_status")
            tel = self.request.user.username
            User.objects.filter(tel=tel).update(send_message_status=send_message_status)
            if send_message_status == "0":
                success_msg = {
                    "result": "短信提醒功能已关闭"
                }
                return Response(success_msg, status=status.HTTP_200_OK)
            elif send_message_status == "1":
                success_msg = {
                    "result": "短信提醒功能已开启"
                }
                return Response(success_msg, status=status.HTTP_200_OK)
            else:
                failure_msg = {
                    "result": "短信状态码发送错误"
                }
                return Response(failure_msg, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            failure_msg = {
                "result": str(e)
            }
            return Response(failure_msg, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return User.objects.filter(username=self.request.username)


class LoginErrorNumViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    查询用户APP登录错误次数 /Basic Auth
    """
    serializer_class = TelInfoSerializer
    authentication_classes = (BasicAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        try:
            tel = request.data.get("tel")
            error_num_app = User.objects.filter(tel=tel).values('error_num_app')
            error_num_app = list(error_num_app)[0]["error_num_app"]
            error_num_app_msg = {
                "result": str(error_num_app)
            }
            return Response(error_num_app_msg, status=status.HTTP_200_OK)
        except Exception as e:
            failmsg = {
                "result": "该号码未注册！"
            }
            return Response(failmsg, status=status.HTTP_400_BAD_REQUEST)


class UserDetailViewset(ListModelMixin, viewsets.GenericViewSet):
    """
      登录APP后获取用户的详细信息
    """
    serializer_class = UserDetailSerializer
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return User.objects.filter(username=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        # 获取教务系统账号对应的名字
        name = User.objects.filter(username=self.request.user).values('name')
        name = list(name)[0]["name"]
        # 获取教务系统的api_key
        api_key = User.objects.filter(username=self.request.user).values('api_key')
        api_key = list(api_key)[0]['api_key']
        # 获取登录教务系统错误次数
        error_num_jw = User.objects.filter(username=self.request.user).values('error_num_jw')
        error_num_jw = list(error_num_jw)[0]['error_num_jw']
        if name == "NULL":
            nullMsg = {
                'msg': '未绑定教务系统账号',
                'body': serializer.data,
                'jwStatus': '1',
                'content':{
                    "alertTitle": "未绑定教务系统账号",
                    "userMessage": "请绑定教务系统账号。",
                    "actionTitle": "前往绑定"
                }
            }
            return Response(nullMsg, status=status.HTTP_400_BAD_REQUEST)
        elif name == "passwordError":
            passwordErrorMsg = {
                'msg': '教务系统账号或密码错误',
                'body': serializer.data,
                'jwStatus': '2',
                'content':{
                    "alertTitle": "密码错误",
                    "userMessage": "对不起，教务系统账号或密码错误，请核实后登陆，如连续错误3次该账号将被锁定。",
                    "actionTitle": "确定"
                }
            }
            return Response(passwordErrorMsg, status=status.HTTP_400_BAD_REQUEST)
        elif name == "notInSchool":
            notInSchoolMsg = {
                'msg': '非在校生',
                'body': serializer.data,
                'jwStatus': '3',
                'content': {
                    "alertTitle": "非在校生",
                    "userMessage": "对不起，教务系统账号处于非在校生状态，目前行走嘉园仅对在校生开开放。",
                    "actionTitle": "确定"
                }
            }
            return Response(notInSchoolMsg, status=status.HTTP_400_BAD_REQUEST)
        elif name == "lock" and int(error_num_jw) >= 3:
            lockMsg = {
                'msg': '账号锁定',
                'body': serializer.data,
                'jwStatus': '5',
                'content':{
                    "alertTitle": "账户被锁定",
                    "userMessage": "对不起，该教务系统账号处于锁定状态，请10分钟后再次尝试登陆",
                    "actionTitle": "确定"
                }
            }
            return Response(lockMsg, status=status.HTTP_400_BAD_REQUEST)
        elif api_key == "NULL" and name != "NULL" and name != "lock":
            notConfirmInfoMsg = {
                'msg': '未确认个人信息',
                'body': serializer.data,
                'jwStatus': '4',
                'content': {
                    "alertTitle": "请确认个人信息",
                    "userMessage": "对不起，请在教务系统网页版确认个人信息后再登陆行走嘉园绑定该账号。",
                    "actionTitle": "确定"
                }
            }
            return Response(notConfirmInfoMsg, status=status.HTTP_400_BAD_REQUEST)
        else:
            jw_result = JWMessageNotice.objects.filter(user=self.request.user.id).filter(read=False)
            app_result = APPMessageNotice.objects.filter(user=self.request.user.id).filter(read=False)
            if jw_result or app_result:
                containUnread = '1'
            else:
                containUnread = '0'
            successMsg = {
                'containUnread': containUnread,
                'msg': 'success',
                'jwStatus': '0',
                'body': serializer.data,
            }
            return Response(successMsg, status=status.HTTP_200_OK)


class UserJwStatusViewset(ListModelMixin, viewsets.GenericViewSet):
    """
    获取教务系统系统爬取状态
    """
    serializer_class = UserDetailSerializer
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return User.objects.filter(username=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        # 获取教务系统账号对应的名字
        name = User.objects.filter(username=self.request.user).values('name')
        name = list(name)[0]["name"]
        # 获取教务系统的api_key
        api_key = User.objects.filter(username=self.request.user).values('api_key')
        api_key = list(api_key)[0]['api_key']
        # 获取爬取教务系统的状态码
        isTryingReLoginJW = User.objects.filter(username=self.request.user).values('isTryingReLoginJW')
        isTryingReLoginJW = list(isTryingReLoginJW)[0]["isTryingReLoginJW"]
        # 获取登录教务系统错误次数
        error_num_jw = User.objects.filter(username=self.request.user).values('error_num_jw')
        error_num_jw = list(error_num_jw)[0]['error_num_jw']
        if isTryingReLoginJW == "1":
            loginMsg = {
                'result': '正在获取教务系统信息，请稍等。',
            }
            return Response(loginMsg, status=status.HTTP_202_ACCEPTED)
        else:
            if name == "passwordError":
                passwordErrorMsg = {
                    'result': '教务系统账号或密码错误，请核实后登陆。如连续错误3次将锁定该账号。',
                }
                return Response(passwordErrorMsg, status=status.HTTP_400_BAD_REQUEST)
            elif name == "notInSchool":
                notInSchoolMsg = {
                    'result': '该账号状态为非在校生，目前行走嘉园仅对嘉庚在校生开放，敬请谅解。',
                }
                return Response(notInSchoolMsg, status=status.HTTP_400_BAD_REQUEST)
            elif name == "lock" and int(error_num_jw) >= 3:
                lockMsg = {
                    'result': '该教务系统账号已被锁定，请10分钟后再次尝试登陆。',
                }
                return Response(lockMsg, status=status.HTTP_400_BAD_REQUEST)
            elif api_key == "NULL" and name != "NULL" and name != "lock":
                notConfirmInfoMsg = {
                    'result': '请在教务系统网页版确认个人信息后再登陆行走嘉园绑定该账号。',
                }
                return Response(notConfirmInfoMsg, status=status.HTTP_400_BAD_REQUEST)
            else:
                successlMsg = {
                    'result': name,
                    'body': serializer.data,
                }
                return Response(successlMsg, status=status.HTTP_200_OK)


class UserJwBindViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    绑定教务系统信息及宿舍信息（宿舍信息可为空）
    """
    serializer_class = UserJwBindSerializer
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        # 选择4个tem表中记录数最少的一个表插入记录
        Tem1 = UserInfo_tem_1.objects.count()
        Tem2 = UserInfo_tem_2.objects.count()
        Tem3 = UserInfo_tem_3.objects.count()
        Tem4 = UserInfo_tem_4.objects.count()
        table_list = [("Tem1", Tem1), ("Tem2", Tem2), ("Tem3", Tem3), ("Tem4", Tem4)]
        tables = sorted(table_list, key=lambda table: table[1])
        table_dict = {
            "Tem1": UserInfo_tem_1,
            "Tem2": UserInfo_tem_2,
            "Tem3": UserInfo_tem_3,
            "Tem4": UserInfo_tem_4,
        }
        tel = self.request.user.username
        username_jw = request.data.get("username_jw")
        password_jw = request.data.get("password_jw")
        password_jw = pc.encrypt(password_jw)
        drxiaoqu = request.data.get("drxiaoqu")
        drlou = request.data.get("drlou")
        drRoomId = request.data.get("drRoomId")
        table_key = tables[0][0]
        table = table_dict[table_key]

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            table.objects.create(tel=tel, username_jw=username_jw, password_jw=password_jw, drxiaoqu=drxiaoqu,
                                 drlou=drlou, drRoomId=drRoomId)
            UserProfile.objects.filter(tel=tel).update(isTryingReLoginJW="1")
            successMsg = {
                'result': '正在获取教务信息，请稍等...',
            }
            return Response(successMsg, status=status.HTTP_200_OK)
        else:
            failMsg = {
                'result': '信息填写错误，请重新尝试。',
            }
            return Response(failMsg, status=status.HTTP_400_BAD_REQUEST)


class LoginViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    登录接口 /Basic Auth
    """
    serializer_class = LoginSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        tel = request.data.get("tel")
        username = tel
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            blacklist = User.objects.filter(username=username).values('blacklist')
            blacklist = list(blacklist)[0]["blacklist"]
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            if blacklist:
                failMsg = {
                    'result': '对不起，您的账号已被禁用。如有疑问请联系 contact@forsource.cn',
                }
                return Response(failMsg, status=status.HTTP_400_BAD_REQUEST)
            else:
                successMsg = {
                    'result': token,
                }
                return Response(successMsg, status=status.HTTP_200_OK)
        else:
            failMsg = {
                'result': '此账号不存在，请先注册~',
            }
            return Response(failMsg, status=status.HTTP_400_BAD_REQUEST)


class UserImageViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    用户上传/修改头像
    """
    serializer_class = UserImageSerializer
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)

    def create(self, request, *args, **kwargs):
        user_id = self.request.user.id
        user_image_base64 = request.data.get("user_image_base64")
        try:
            # user_image_url = "NULL"
            if user_image_base64:
                upload_image = UploadImageOssStorage("walkingtkk-user-image")
                filename = self.request.user.username
                filename = filename + "_user_image.png"
                imgdata = base64.b64decode(user_image_base64)
                with open(filename, 'wb') as f:
                    f.write(imgdata)
                f.close()
                user_image_url = upload_image.save(filename, filename)
                # print(user_image_url)
                os.remove(filename)

                UserProfile.objects.filter(id=user_id).update(user_image_url=user_image_url)
                SuccessMsg = {
                    "result": "头像修改成功",
                    "user_image_url": user_image_url,
                }
                return Response(SuccessMsg, status=status.HTTP_200_OK)
        except Exception as e:
            FailMsg = {
                "result": "头像修改失败，请稍后尝试。"
            }
            return Response(FailMsg, status=status.HTTP_400_BAD_REQUEST)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    # max_page_size = 1000


class UserinfoUpdateViewset(ListModelMixin, viewsets.GenericViewSet):
    """
    获取用户教务系统信息，用于更新教务系统信息，仅供服务器使用!
    """
    serializer_class = UserinfoUpdateSerializer
    authentication_classes = (BasicAuthentication,)
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return User.objects.all()


class UserinfoQuery1Viewset(ListModelMixin, viewsets.GenericViewSet):
    """
    1.获取用户教务系统临时信息，仅供服务器使用!
    """
    serializer_class = UserInfoTem1Serializer
    authentication_classes = (BasicAuthentication,)

    def get_queryset(self):
        return UserInfo_tem_1.objects.all()


class UserinfoQuery2Viewset(ListModelMixin, viewsets.GenericViewSet):
    """
    2.获取用户教务系统临时信息，仅供服务器使用!
    """
    serializer_class = UserInfoTem1Serializer
    authentication_classes = (BasicAuthentication,)

    def get_queryset(self):
        return UserInfo_tem_2.objects.all()


class UserinfoQuery3Viewset(ListModelMixin, viewsets.GenericViewSet):
    """
    3.获取用户教务系统临时信息，仅供服务器使用!
    """
    serializer_class = UserInfoTem1Serializer
    authentication_classes = (BasicAuthentication,)

    def get_queryset(self):
        return UserInfo_tem_3.objects.all()


class UserinfoQuery4Viewset(ListModelMixin, viewsets.GenericViewSet):
    """
    4.获取用户教务系统临时信息，仅供服务器使用!
    """
    serializer_class = UserInfoTem1Serializer
    authentication_classes = (BasicAuthentication,)

    def get_queryset(self):
        return UserInfo_tem_4.objects.all()


class UserLoginInfoCheckViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    获取爬取用户登录时的必要信息，仅供服务器使用!
    """
    serializer_class = UserLoginInfoCheckSerializer
    authentication_classes = (BasicAuthentication,)

    def create(self, request, *args, **kwargs):
        tel = request.data.get("tel")
        user_info = User.objects.filter(tel=tel).values()
        user_id = user_info[0]["id"]
        username_jw = user_info[0]["username_jw"]
        error_num_jw = user_info[0]["error_num_jw"]
        if user_info:
            msg = {
                "id": user_id,
                "username_jw": username_jw,
                "error_num_jw": error_num_jw
            }
            return Response(msg, status=status.HTTP_200_OK)
        else:
            fail_msg = {
                "result": "未搜索到该用户信息"
            }
            return Response(fail_msg, status=status.HTTP_400_BAD_REQUEST)


class CurrentWeekViewset(ListModelMixin, viewsets.GenericViewSet):
    """
    查询当前周数
    """
    serializer_class = CurrentWeekSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        return User.objects.filter(username=self.request.user)


class AddUserViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    添加用户，用于用户信息转移/Basic Auth
    """
    serializer_class = AddUserSerializer
    queryset = User.objects.all()
    authentication_classes = (BasicAuthentication, SessionAuthentication)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        username = request.data.get("username")
        tel = request.data.get("tel")
        password = request.data.get("password")
        password_jw = request.data.get("password")
        if username != tel:
            fail_msg = {
                "result": "username与tel不一致，请前端开发人员注意(微笑脸)"
            }
            return Response(fail_msg, status=status.HTTP_400_BAD_REQUEST)
        elif UserProfile.objects.filter(username=username):
            fail_msg = {
                "result": "该账号已注册，快去登录吧。"
            }
            return Response(fail_msg, status=status.HTTP_400_BAD_REQUEST)
        elif len(username) == 0 or len(password) == 0 or len(tel) == 0:
            fail_msg = {
                "result": "请填写所有内容！"
            }
            return Response(fail_msg, status=status.HTTP_400_BAD_REQUEST)
        elif len(username) != 11 or len(tel) != 11:
            fail_msg = {
                "result": "请填写正确的手机号码，暂时只支持中国大陆手机号码哦！"
            }
            return Response(fail_msg, status=status.HTTP_400_BAD_REQUEST)
        elif len(password) < 8 or len(password) > 32:
            fail_msg = {
                "result": "密码长度不能小于8位或大于32位哦~"
            }
            return Response(fail_msg, status=status.HTTP_400_BAD_REQUEST)

        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        # 将用户的密码以密文形式备份
        password_app = pc.encrypt(password)
        password_jw = pc.encrypt(password_jw)
        UserProfile.objects.filter(tel=tel).update(password_app=password_app, password_jw=password_jw)
        success_msg = {
            "result": "注册成功！赶快去登录吧 ^_^"
        }
        return Response(success_msg, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        return serializer.save()







