"""
This app view is for PE attendance
"""

from datetime import datetime
from django.shortcuts import render

from rest_framework import status
from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin, ListModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.pagination import PageNumberPagination

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import AccountTemSerializer, AccountSerializer, AttentanceNumSerializer, DeleteAccountTemSerializer, \
    AccountTemServerSerializer
from .models import UserAccountTem, UserAccount, AttentanceNum
# Create your views here.

time_now = datetime.now()

class PeAccountTemViewset(CreateModelMixin, ListModelMixin, DestroyModelMixin, viewsets.GenericViewSet):
    """
    金教电子账号临时信息；
    客户端使用post上传用户信息；
    服务器使用get获取用户信息及delete删除用户信息；
    """
    serializer_class = AccountTemSerializer
    queryset = UserAccountTem.objects.all()
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication, BasicAuthentication)

    def get_serializer_class(self):
        if self.action == "list":
            return AccountTemServerSerializer
        elif self.action == "create":
            return AccountTemSerializer
        return AccountTemServerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        username_pe = request.data.get("username_pe")
        username_pe = str.upper(username_pe)
        password_pe = request.data.get("password_pe")
        if len(username_pe) == 0 or len(password_pe) == 0:
            fail_msg = {
                "result": "请填写所有信息！"
            }
            return Response(fail_msg, status=status.HTTP_400_BAD_REQUEST)
        if len(username_pe) != 8:
            fail_msg = {
                "result": "请检查学号是否输入正确！"
            }
            return Response(fail_msg, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            if UserAccount.objects.filter(user_id=self.request.user.id):
                UserAccount.objects.filter(user_id=self.request.user.id).update(username_pe=username_pe,
                                                                                password_pe=password_pe, status="0", crawl_time=time_now)
            else:
                UserAccount.objects.create(username_pe=username_pe, password_pe=password_pe, status="0", crawl_time=time_now,
                                           user_id=self.request.user.id)
            success_msg = {
                "result": "金教电子账号信息已提交，请耐心等待~"
            }
            return Response(success_msg, status=status.HTTP_201_CREATED)


class PeAccountViewset(ListModelMixin, CreateModelMixin, viewsets.GenericViewSet):
    """
    金教电子账号信息；
    客户端使用get获取用户信息，默认为NULL；
    服务器使用post上传用户信息；status：0(默认)->正在爬取信息, 1->爬取成功, 2->账号或密码错误, 3->其他错误
    """
    serializer_class = AccountSerializer
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication, BasicAuthentication)

    def list(self, request, *args, **kwargs):
        user_account_result = UserAccount.objects.filter(user=self.request.user.id)
        if user_account_result:
            user_account_result = user_account_result.values()[0]
            account_status = user_account_result["status"]
            username_pe = user_account_result["username_pe"]
            password_pe = user_account_result["password_pe"]
            if account_status == "0":
                # fail_msg = {
                #     "result": "系统升级中，请小主稍安勿躁~"
                # }
                fail_msg = {
                    "result": "正在获取出勤信息，请稍等~"
                }
                return Response(fail_msg, status=status.HTTP_202_ACCEPTED)
            if account_status == "1":
                success_msg = {
                    "username_pe": username_pe,
                    "password_pe": password_pe,
                    "status": account_status,
                }
                return Response(success_msg, status=status.HTTP_200_OK)
            if account_status == "2":
                fail_msg = {
                    "result": "金教电子账号或密码错误，请核对后再绑定。账号中的字母需要大写哦~"
                }
                return Response(fail_msg, status=status.HTTP_400_BAD_REQUEST)
            else:
                fail_msg = {
                    "result": "服务器正忙，请稍后尝试~"
                }
                return Response(fail_msg, status=status.HTTP_400_BAD_REQUEST)
        else:
            fail_msg = {
                "result": "需要先绑定金教电子账号哦~"
            }
            # fail_msg = {
            #     "result": "系统升级中，请小主稍安勿躁~"
            # }
            return Response(fail_msg, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        username_pe = request.data.get("username_pe")
        password_pe = request.data.get("password_pe")
        account_status = request.data.get("status")
        user_id = request.data.get("user")
        user_account_result = UserAccount.objects.filter(user_id=user_id)
        if user_account_result and user_id:
            UserAccount.objects.filter(user_id=user_id).update(username_pe=username_pe, password_pe=password_pe, status=account_status,
                                                               crawl_time=time_now)
        else:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        success_msg = {
            "result": "账号信息已修改。"
        }
        return Response(success_msg, status=status.HTTP_200_OK)


class AttentanceNumViewset(ListModelMixin, CreateModelMixin, viewsets.GenericViewSet):
    """
    体育出勤信息；
    客户端使用get获取用户信息，默认为NULL；
    服务器使用post上传用户信息；
    """
    serializer_class = AttentanceNumSerializer
    authentication_classes = (BasicAuthentication, JSONWebTokenAuthentication)

    def get_queryset(self):
        return AttentanceNum.objects.filter(user=self.request.user.id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        user_id = request.data.get("user")
        one = request.data.get("one")
        three = request.data.get("three")
        five = request.data.get("five")
        seven = request.data.get("seven")
        nine = request.data.get("nine")
        zj = request.data.get("zj")
        bk = request.data.get("bk")
        sum = request.data.get("sum")
        last_sum = request.data.get("last_sum")
        user_attentance= AttentanceNum.objects.filter(user_id=user_id)
        if user_attentance and user_id:
            AttentanceNum.objects.filter(user_id=user_id).update(one=one, three=three, five=five, seven=seven, nine=nine,
                                                               zj=zj, bk=bk, sum=sum, last_sum=last_sum, crawl_time=time_now)
        elif not sum and not bk:
            fail_msg = {
                "result": "信息修改不成功"
            }
            return Response(fail_msg, status=status.HTTP_200_OK)
        else:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        success_msg = {
            "result": "账号信息已修改。"
        }
        return Response(success_msg, status=status.HTTP_200_OK)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    # max_page_size = 1000

class GetAllPeAccountViewset(ListModelMixin, viewsets.GenericViewSet):
    """
    体育出勤信息；
    客户端使用get获取用户信息，默认为NULL；
    服务器使用post上传用户信息；
    """
    serializer_class = AccountSerializer
    authentication_classes = (BasicAuthentication, SessionAuthentication)
    queryset = UserAccount.objects.all()
    pagination_class = StandardResultsSetPagination


class DeletePeAccountTemViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    通过postid删除用户临时账号信息；
    """
    serializer_class = DeleteAccountTemSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        record_id = request.data.get("id")
        serializer.is_valid(raise_exception=True)
        try:
            UserAccountTem.objects.filter(id=record_id).delete()
            success_msg = {
                "result": "临时账号信息已删除"
            }
            return Response(success_msg, status=status.HTTP_200_OK)
        except Exception as e:
            fail_msg = {
                "result": "临时账号信息删除失败，" + str(e)
            }
            return Response(fail_msg, status=status.HTTP_400_BAD_REQUEST)

