"""
This app view is for Student Affairs System
"""

from rest_framework import mixins
from rest_framework import viewsets

from rest_framework.permissions import IsAuthenticated

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication


from .models import Grade, TermInfo, Attendance, ClassSwitch, Exam
from .serializers import GradeSerializer, TermInfoSerializer, AttendanceSerializer, ClassSwitchSerializer, \
    ExamSerializer
# Create your views here.


class GradeViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    用户成绩信息
    """
    # queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)

    def get_queryset(self):
        return Grade.objects.filter(user=self.request.user)


class CurriculumViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    用户课表信息
    """
    serializer_class = TermInfoSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)

    def get_queryset(self):
        return TermInfo.objects.filter(user=self.request.user)


class AttendanceViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    用户出勤信息
    """
    serializer_class = AttendanceSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)

    def get_queryset(self):
        return Attendance.objects.filter(user=self.request.user)


class ClassSwitchViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    用户调停补课信息
    """
    serializer_class = ClassSwitchSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)

    def get_queryset(self):
        return ClassSwitch.objects.filter(user=self.request.user).order_by("-id")


class ExamViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    用户考试安排信息
    """
    serializer_class = ExamSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)

    def get_queryset(self):
        return Exam.objects.filter(user=self.request.user)





