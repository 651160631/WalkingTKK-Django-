"""
This app view is for User Operation
"""

from django.contrib.auth import get_user_model
from django.db.models import Count

from rest_framework import status
from rest_framework import viewsets
from rest_framework import filters

from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework_jwt.authentication import JSONWebTokenAuthentication


from .serializers import PushSettingsSerializer, PushSettingsQuerySerializer, UserInfoDeleteSerializer, \
    UserLoginInfoSerializer, UpdateStatisticsSerializer

from .models import PushSettings, LoginInfo, UserRegistrationStatistics, UserLoginStatistics

User = get_user_model()


class PushSettingsViewset(CreateModelMixin, ListModelMixin, viewsets.GenericViewSet):
    """
    极光推送，用户id上传与查询;
    iOS和Android使用同一个接口；客户端只使用post功能
    post数据中必须包含id_ios和id_android这两个key
    注意若苹果手机上传则id_android为"NULL"，安卓手机上传则id_ios为"NULL"
    """
    queryset = PushSettings.objects.all()
    serializer_class = PushSettingsSerializer
    authentication_classes = (JSONWebTokenAuthentication, BasicAuthentication, SessionAuthentication)
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filter_fields = ('tel',)
    search_fields = ('id_ios', 'tel', 'id_android')

    def get_serializer_class(self):
        if self.action == "list":
            return PushSettingsQuerySerializer
        elif self.action == "create":
            return PushSettingsSerializer
        return PushSettingsSerializer

    def create(self, request, *args, **kwargs):
        user_id = self.request.user.id
        if user_id:
            id_ios = request.data.get("id_ios")
            id_android = request.data.get("id_android")
            username_jw = User.objects.filter(id=user_id).values("username_jw")[0]["username_jw"]
            tel = User.objects.filter(id=user_id).values("tel")[0]["tel"]
            if username_jw != "NULL":
                grade = "20" + username_jw[3:5]
            else:
                grade = "NULL"
            record = PushSettings.objects.filter(user=self.request.user)
            if record:
                id_ios_raw = PushSettings.objects.filter(user=self.request.user).values("id_ios")[0]["id_ios"]
                id_android_raw = PushSettings.objects.filter(user=self.request.user).values("id_android")[0]["id_android"]
                if id_ios_raw != "NULL" and id_ios == "NULL":
                    id_ios = id_ios_raw
                if not id_ios:
                    id_ios = id_ios_raw
                if id_android_raw != "NULL" and id_android == "NULL":
                    id_android = id_android_raw
                if not id_android:
                    id_android = id_android_raw
                PushSettings.objects.filter(user=self.request.user).update(
                    tel=tel,
                    id_ios=id_ios,
                    id_android=id_android,
                    tag_grade=grade
                )
                msg = {
                    "result": "id上传成功！"
                }
                return Response(msg, status=status.HTTP_200_OK)
            else:
                PushSettings.objects.filter(user=self.request.user).create(
                    user_id=user_id,
                    tel=tel,
                    id_ios=id_ios,
                    id_android=id_android,
                    tag_grade=grade
                )
                msg = {
                    "result": "id上传成功！"
                }
                return Response(msg, status=status.HTTP_200_OK)
        else:
            failmsg = {
                "result": "不存在该用户"
            }
            return Response(failmsg, status=status.HTTP_400_BAD_REQUEST)


class UserInfoDeleteViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    一键删除用户信息，不可撤销
    """
    serializer_class = UserInfoDeleteSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tel = request.data.get("tel")

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserLoginInfoViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    上传用户登录信息（日志）
    """
    serializer_class = UserLoginInfoSerializer
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        success_msg = {
            "result": "上传成功"
        }
        return Response(success_msg, status=status.HTTP_201_CREATED, headers=headers)


class UpdateStatisticsViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    更新统计数据（服务器）
    """
    serializer_class = UpdateStatisticsSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def update_login_statistics(self):
        login_nums = LoginInfo.objects.extra({'login_time_app': "date(login_time_app)"}).values(
            'login_time_app').annotate(
            number=Count('id'))
        people_nums = LoginInfo.objects.extra({'login_time_app': "date(login_time_app)"}).values(
            'login_time_app').annotate(
            p_number=Count('user_id', distinct=True))
        for login_num in login_nums:
            login_date = login_num["login_time_app"]
            login_people_num = login_num["number"]
            user_login = UserLoginStatistics(login_date=login_date, page_view=login_people_num)
            user_login.save()
        for people_num in people_nums:
            login_date = people_num["login_time_app"]
            p_number = people_num["p_number"]
            UserLoginStatistics.objects.filter(login_date=login_date).update(unique_visitor=p_number)

    def update_reg_statistics(self):
        reg_nums = User.objects.extra({'registerTime': "date(registerTime)"}).values('registerTime').annotate(
            number=Count('id'))
        for reg in reg_nums:
            registerTime = reg["registerTime"]
            reg_num = reg["number"]
            user_login = UserRegistrationStatistics(reg_date=registerTime, people_number=reg_num)
            user_login.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.update_reg_statistics()
            self.update_login_statistics()
            success_msg = {
                "result": "更新成功"
            }
            return Response(success_msg, status=status.HTTP_200_OK)
        except Exception as e:
            fail_msg = {
                "result": "更新失败 - " + str(e)
            }
            return Response(fail_msg, status=status.HTTP_400_BAD_REQUEST)
