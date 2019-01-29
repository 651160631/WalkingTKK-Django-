"""
This app view is for Client
"""

from datetime import datetime
import os


from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework import viewsets
from rest_framework import filters

from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from django_filters.rest_framework import DjangoFilterBackend

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

from .serializers import SuggestionSerializer, MessageNoticeSerializer, AppLaunchImageCommonSerializer, \
    AppLaunchImageLatestSerializer, JWMessageGroupNoticeSerializer, JWMessageNoticeSerializer, \
    APPMessageGroupNoticeSerializer, APPMessageNoticeSerializer, APPMessageReadSerializer, JWMessageReadSerializer, \
    JWMessagePushOneSerializer, ErrorLogSerializer, APPMessagePushOneSerializer
from .models import Suggestion, MessageNotice, AppLaunchImageLatest, AppLaunchImageCommon, APPMessageNotice, \
     JWMessageNotice
from user_operation.models import PushSettings

from utils.permissions import IsOwnerOrReadOnly
from utils.uoload_file_alioss import UploadImageOssStorage
from utils.jg_push import notification_one
from utils.jg_push import notification_all

User = get_user_model()
upload_image = UploadImageOssStorage("walkingtkk-suggestion")


# Create your views here.

class SuggestionViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    用户建议与反馈(至多添加5张截图)
    """
    serializer_class = SuggestionSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return Suggestion.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            user_id = self.request.user.id
            content = request.data.get("content")
            image_1 = request.data.get("image_1")
            image_2 = request.data.get("image_2")
            image_3 = request.data.get("image_3")
            image_4 = request.data.get("image_4")
            image_5 = request.data.get("image_5")
            image_1_url = "NULL"
            image_2_url = "NULL"
            image_3_url = "NULL"
            image_4_url = "NULL"
            image_5_url = "NULL"
            if image_1:
                filename = 'suggestion/' + self.request.user.username + "_" + str(datetime.now()).replace(" ", "")
                filename = filename + "_image_1.png"
                filepath = default_storage.save(filename, ContentFile(image_1.read()))
                filename = os.path.join(settings.MEDIA_ROOT, filepath)
                image_1_url = upload_image.save(os.path.basename(filename), filename)
                os.remove(filename)
            if image_2:
                filename = 'suggestion/' + self.request.user.username + "_" + str(datetime.now()).replace(" ", "")
                filename = filename + "_image_2.png"
                filepath = default_storage.save(filename, ContentFile(image_2.read()))
                filename = os.path.join(settings.MEDIA_ROOT, filepath)
                image_2_url = upload_image.save(os.path.basename(filename), filename)
                os.remove(filename)
            if image_3:
                filename = 'suggestion/' + self.request.user.username + "_" + str(datetime.now()).replace(" ", "")
                filename = filename + "_image_3.png"
                filepath = default_storage.save(filename, ContentFile(image_3.read()))
                filename = os.path.join(settings.MEDIA_ROOT, filepath)
                image_3_url = upload_image.save(os.path.basename(filename), filename)
                os.remove(filename)
            if image_4:
                filename = 'suggestion/' + self.request.user.username + "_" + str(datetime.now()).replace(" ", "")
                filename = filename + "_image_4.png"
                filepath = default_storage.save(filename, ContentFile(image_4.read()))
                filename = os.path.join(settings.MEDIA_ROOT, filepath)
                image_4_url = upload_image.save(os.path.basename(filename), filename)
                os.remove(filename)
            if image_5:
                filename = 'suggestion/' + self.request.user.username + "_" + str(datetime.now()).replace(" ", "")
                filename = filename + "_image_5.png"
                filepath = default_storage.save(filename, ContentFile(image_5.read()))
                filename = os.path.join(settings.MEDIA_ROOT, filepath)
                image_5_url = upload_image.save(os.path.basename(filename), filename)
                os.remove(filename)
            Suggestion.objects.create(user_id=user_id, content=content, image_1_url=image_1_url, image_2_url=image_2_url,
                                      image_3_url=image_3_url, image_4_url=image_4_url, image_5_url=image_5_url)
            SuccessMsg = {
                "result": "感谢您的宝贵建议，我们会尽快与您取得联系并解决问题。"
            }
            return Response(SuccessMsg, status=status.HTTP_201_CREATED)
        except Exception as e:
            failMsg = {
                "result": "图片上传错误，请重试。 " + str(e)
            }
            return Response(failMsg, status=status.HTTP_400_BAD_REQUEST)


class MessageNoticeViewset(ListModelMixin, viewsets.GenericViewSet):
    """
    通知客户端的信息，注意匹配不同版本，默认为NULL；
    """
    serializer_class = MessageNoticeSerializer
    authentication_classes = (BasicAuthentication, SessionAuthentication)
    queryset = MessageNotice.objects.all().order_by('-id')


class AppLaunchImageCommonViewset(ListModelMixin, viewsets.GenericViewSet):
    """
    客户端启动页 - 日常普通图片；
    当有多个的时候，客户端每次启动从其中选择一个出来；
    客户端在启动后将服务器中图片的id与本地的id比对，和服务器保持一致；
    """
    serializer_class = AppLaunchImageCommonSerializer
    authentication_classes = (BasicAuthentication, SessionAuthentication)
    queryset = AppLaunchImageCommon.objects.all().order_by('-id')

    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filter_fields = ('platform', 'size')


class AppLaunchImageLatestViewset(ListModelMixin, viewsets.GenericViewSet):
    """
    客户端启动页 - 最新节日/活动图片，包含起止日期；
    当有多个的时候，客户端每次启动从其中选择一个出来；
    """
    serializer_class = AppLaunchImageLatestSerializer
    authentication_classes = (BasicAuthentication, SessionAuthentication)
    queryset = AppLaunchImageLatest.objects.all().order_by('-id')

    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filter_fields = ('platform', 'size')


class JWMessageNoticeViewset(ListModelMixin, viewsets.GenericViewSet):
    """
    查询关于教务系统的推送消息；
    """
    serializer_class = JWMessageNoticeSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return JWMessageNotice.objects.filter(user=self.request.user).order_by('-id')


class APPMessageNoticeViewset(ListModelMixin, viewsets.GenericViewSet):
    """
    查询关于APP的推送消息；
    """
    serializer_class = APPMessageNoticeSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return APPMessageNotice.objects.filter(user=self.request.user).order_by('-id')


class JWMessageNoticeGroupViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    教务系统消息推送(群发)；
    服务器使用POST功能；
    """
    serializer_class = JWMessageGroupNoticeSerializer
    authentication_classes = (BasicAuthentication, SessionAuthentication)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            content = request.data.get("content")
            all_student = request.data.get("all_student")
            grade = request.data.get("grade")
            user_ids = User.objects.all().values_list('id')
            if all_student:
                for user_id in user_ids:
                    user_id = user_id[0]
                    user_push_info = PushSettings.objects.filter(user_id=user_id)
                    if user_push_info:
                        JWMessageNotice.objects.create(user_id=user_id, content=content)
                push_result = notification_all(msg=content, type='jw')
                if push_result:
                    failMsg = {
                        "result": push_result
                    }
                    return Response(failMsg, status=status.HTTP_400_BAD_REQUEST)
                else:
                    serializer.is_valid(raise_exception=True)
                    self.perform_create(serializer)
                    SuccessMsg = {
                        "result": "推送成功"
                    }
                    return Response(SuccessMsg, status=status.HTTP_201_CREATED)
            else:
                push_result = None
                for user_id in user_ids:
                    user_id = user_id[0]
                    user_push_info = PushSettings.objects.filter(user_id=user_id).values()
                    if user_push_info:
                        ios_reg_id = user_push_info[0]["id_ios"]
                        android_reg_id = user_push_info[0]["id_android"]
                        tag_grade = user_push_info[0]["tag_grade"]
                        if grade == tag_grade:
                            JWMessageNotice.objects.create(user_id=user_id, content=content)
                            if ios_reg_id != "NULL":
                                push_result = notification_one(reg_id=ios_reg_id, msg=content, type='jw')
                            if android_reg_id != "NULL":
                                push_result = notification_one(reg_id=android_reg_id, msg=content, type='jw')
                if push_result:
                    failMsg = {
                        "result": push_result
                    }
                    return Response(failMsg, status=status.HTTP_400_BAD_REQUEST)
                else:
                    serializer.is_valid(raise_exception=True)
                    self.perform_create(serializer)
                    SuccessMsg = {
                        "result": "推送成功"
                    }
                    return Response(SuccessMsg, status=status.HTTP_201_CREATED)
        except Exception as e:
            failMsg = {
                "result": "接口调用失败, 原因：" + str(e)
            }
            return Response(failMsg, status=status.HTTP_400_BAD_REQUEST)


class APPMessageNoticeGroupViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    APP消息推送(群发)；
    服务器使用POST功能；
    """
    serializer_class = APPMessageGroupNoticeSerializer
    authentication_classes = (BasicAuthentication, SessionAuthentication)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            title = request.data.get("title")
            content = request.data.get("content")
            all_student = request.data.get("all_student")
            grade = request.data.get("grade")
            user_ids = User.objects.all().values_list('id')
            if all_student:
                for user_id in user_ids:
                    user_id = user_id[0]
                    user_push_info = PushSettings.objects.filter(user_id=user_id)
                    if user_push_info:
                        APPMessageNotice.objects.create(user_id=user_id, title=title, content=content)
                push_result = notification_all(msg=title, type='app')
                if push_result:
                    failMsg = {
                        "result": push_result
                    }
                    return Response(failMsg, status=status.HTTP_400_BAD_REQUEST)
                else:
                    serializer.is_valid(raise_exception=True)
                    self.perform_create(serializer)
                    SuccessMsg = {
                        "result": "推送成功"
                    }
                    return Response(SuccessMsg, status=status.HTTP_201_CREATED)
            else:
                push_result = None
                for user_id in user_ids:
                    user_id = user_id[0]
                    user_push_info = PushSettings.objects.filter(user_id=user_id).values()
                    if user_push_info:
                        ios_reg_id = user_push_info[0]["id_ios"]
                        android_reg_id = user_push_info[0]["id_android"]
                        tag_grade = user_push_info[0]["tag_grade"]
                        if grade == tag_grade:
                            APPMessageNotice.objects.create(user_id=user_id, title=title, content=content)
                            if ios_reg_id != "NULL":
                                push_result = notification_one(reg_id=ios_reg_id, msg=title, type='app')
                            if android_reg_id != "NULL":
                                push_result = notification_one(reg_id=android_reg_id, msg=title, type='app')
                if push_result:
                    failMsg = {
                        "result": push_result
                    }
                    return Response(failMsg, status=status.HTTP_400_BAD_REQUEST)
                else:
                    serializer.is_valid(raise_exception=True)
                    self.perform_create(serializer)
                    SuccessMsg = {
                        "result": "APP消息推送成功"
                    }
                    return Response(SuccessMsg, status=status.HTTP_201_CREATED)
        except Exception as e:
            failMsg = {
                "result": "接口调用失败, 原因：" + str(e)
            }
            return Response(failMsg, status=status.HTTP_400_BAD_REQUEST)


class JWMessageNoticePushViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    教务系统消息推送(单条发送)；
    服务器使用POST功能；
    """
    serializer_class = JWMessagePushOneSerializer
    authentication_classes = (BasicAuthentication, SessionAuthentication)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            content = request.data.get("content")
            user_id = request.data.get("user")
            user_push_info = PushSettings.objects.filter(user_id=user_id).values()
            if user_push_info:
                ios_reg_id = user_push_info[0]["id_ios"]
                android_reg_id = user_push_info[0]["id_android"]
                push_result = None
                if ios_reg_id != "NULL":
                    push_result = notification_one(reg_id=ios_reg_id, msg=content, type='jw')
                if android_reg_id != "NULL":
                    push_result = notification_one(reg_id=android_reg_id, msg=content, type='jw')
                if push_result:
                    failMsg = {
                        "result": push_result
                    }
                    return Response(failMsg, status=status.HTTP_400_BAD_REQUEST)
                else:
                    serializer.is_valid(raise_exception=True)
                    self.perform_create(serializer)
                    SuccessMsg = {
                        "result": "推送成功"
                    }
                    return Response(SuccessMsg, status=status.HTTP_201_CREATED)
        except Exception as e:
            failMsg = {
                "result": "接口调用失败, 原因：" + str(e)
            }
            return Response(failMsg, status=status.HTTP_400_BAD_REQUEST)


class APPMessageNoticePushViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    平台消息推送(单条发送)；
    服务器使用POST功能；
    """
    serializer_class = APPMessagePushOneSerializer
    authentication_classes = (BasicAuthentication, SessionAuthentication)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            title = request.data.get("title")
            content = request.data.get("content")
            tel = request.data.get("tel")
            user_info = User.objects.filter(tel=tel).values()
            if user_info:
                user_id = user_info[0]['id']
                user_push_info = PushSettings.objects.filter(user_id=user_id).values()
                if user_push_info:
                    ios_reg_id = user_push_info[0]["id_ios"]
                    android_reg_id = user_push_info[0]["id_android"]
                    push_result = None
                    if ios_reg_id != "NULL":
                        push_result = notification_one(reg_id=ios_reg_id, msg=title, type='app')
                    if android_reg_id != "NULL":
                        push_result = notification_one(reg_id=android_reg_id, msg=title, type='app')
                    if push_result:
                        failMsg = {
                            "result": push_result
                        }
                        return Response(failMsg, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        serializer.is_valid(raise_exception=True)
                        APPMessageNotice.objects.create(user_id=user_id, title=title, content=content)
                        #self.perform_create(serializer)
                        SuccessMsg = {
                            "result": "APP消息推送成功"
                        }
                        return Response(SuccessMsg, status=status.HTTP_201_CREATED)
            else:
                failMsg = {
                    "result": "请检查手机号码时候输入正确"
                }
                return Response(failMsg, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            failMsg = {
                "result": "接口调用失败, 原因：" + str(e)
            }
            return Response(failMsg, status=status.HTTP_400_BAD_REQUEST)


class JWMessageReadViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    标记用户已阅读教务系统消息(全部置为已阅);
    post read:True 至服务器
    """
    serializer_class = JWMessageReadSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def create(self, request, *args, **kwargs):
        try:
            read = request.data.get("read")
            if read:
                JWMessageNotice.objects.filter(user=self.request.user.id).update(read=True)
                SuccessMsg = {
                    "result": "消息阅读状态更改成功"
                }
                return Response(SuccessMsg, status=status.HTTP_200_OK)
            else:
                failMsg = {
                    "result": "read字段内容上传错误"
                }
                return Response(failMsg, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            failMsg = {
                "result": "接口调用失败, 原因：" + str(e)
            }
            return Response(failMsg, status=status.HTTP_400_BAD_REQUEST)


class APPMessageReadViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    标记用户已阅读APP消息;
    post read:True 至服务器
    """
    serializer_class = APPMessageReadSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def create(self, request, *args, **kwargs):
        try:
            msg_id = request.data.get("msg_id")
            read = request.data.get("read")
            if read:
                APPMessageNotice.objects.filter(id=msg_id, user=self.request.user.id).update(read=True)
                SuccessMsg = {
                    "result": "消息阅读状态更改成功"
                }
                return Response(SuccessMsg, status=status.HTTP_200_OK)
            else:
                failMsg = {
                    "result": "read字段内容上传错误"
                }
                return Response(failMsg, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            failMsg = {
                "result": "接口调用失败, 原因：" + str(e)
            }
            return Response(failMsg, status=status.HTTP_400_BAD_REQUEST)


class JWMessageOneNoticeViewset(ListModelMixin, viewsets.GenericViewSet):
    """
    获取最新一条教务系统的推送消息；
    """
    serializer_class = JWMessageNoticeSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        if JWMessageNotice.objects.filter(user=self.request.user):
            data = JWMessageNotice.objects.filter(user=self.request.user).order_by('-id')[0:1]
            print(data)
            return data
        else:
            return JWMessageNotice.objects.filter(user=self.request.user)


class APPMessageOneNoticeViewset(ListModelMixin, viewsets.GenericViewSet):
    """
    获取最新一条APP的推送消息；
    """
    serializer_class = APPMessageNoticeSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        if APPMessageNotice.objects.filter(user=self.request.user):
            return APPMessageNotice.objects.filter(user=self.request.user).order_by('-id')[0:1]
        else:
            return APPMessageNotice.objects.filter(user=self.request.user)


class ErrorLogViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    上传客户端Bug记录
    """
    serializer_class = ErrorLogSerializer
    authentication_classes = (BasicAuthentication, JSONWebTokenAuthentication, SessionAuthentication)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        success_msg = {
            "result": "上传成功"
        }
        return Response(success_msg, status=status.HTTP_201_CREATED)




