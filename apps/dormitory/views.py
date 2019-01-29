"""
This app view is for Dormitory Information
"""

from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import viewsets

from rest_framework.permissions import IsAuthenticated

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


from .models import ElectricCharge, DormInfo_tem
from .serializers import ElectricChargeSerializer, DormInfoTemSerializer
from utils.permissions import IsOwnerOrReadOnly


class ElectricChargeViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    用户宿舍电费信息
    """
    serializer_class = ElectricChargeSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)

    def get_queryset(self):
        return ElectricCharge.objects.filter(user=self.request.user)


class DormInfoTemViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    添加/修改用户宿舍信息，服务器会将原信息删除，并添加新的宿舍电费信息。必须发送正确格式！！！
    """
    serializer_class = DormInfoTemSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        tel = request.data.get("tel")
        drxiaoqu = request.data.get("drxiaoqu")
        drlou = request.data.get("drlou")
        drRoomId = request.data.get("drRoomId")
        print("roomid is " + str(drRoomId))
        if len(tel) == 0 or len(drxiaoqu) == 0 or len(drlou) == 0 or len(drRoomId) == 0:
            fail_msg = {
                "result": "请填写所有信息！"
            }
            return Response(fail_msg, status=status.HTTP_400_BAD_REQUEST)
        elif len(drRoomId) != 4:
            fail_msg = {
                "result": "宿舍编号为4位数！"
            }
            return Response(fail_msg, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            success_msg = {
                "result": "宿舍信息已提交，请耐心等待~"
            }
            return Response(success_msg, status=status.HTTP_201_CREATED)


class DormInfoTemQueryViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    查询宿舍信息临时表内容（服务器使用）
    """
    serializer_class = DormInfoTemSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (BasicAuthentication, SessionAuthentication)

    def get_queryset(self):
        return DormInfo_tem.objects.all()
