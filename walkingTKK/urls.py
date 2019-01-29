"""walkingTKK URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

import xadmin
from django.conf.urls import url, include
from walkingTKK.settings import MEDIA_ROOT
from django.views.static import serve

from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter, SimpleRouter

# Student Affairs System
from jiaowu.views import GradeViewset, CurriculumViewset, AttendanceViewset, ClassSwitchViewset, ExamViewset

# Dormitary
from dormitory.views import ElectricChargeViewset, DormInfoTemViewset, DormInfoTemQueryViewset

# User
from users.views import SmsCodeViewset, UserRegViewset, TelInfoViewset, PasswordChangeWithKnowRawViewset, \
    PasswordChangeWithSmsViewset, SmsSwitchViewset, LoginErrorNumViewset, UserDetailViewset, UserJwStatusViewset, \
    UserJwBindViewset, LoginViewset, UserImageViewset, UserinfoUpdateViewset, UserinfoQuery1Viewset,\
    UserinfoQuery2Viewset, UserinfoQuery3Viewset, UserinfoQuery4Viewset, UserLoginInfoCheckViewset, CurrentWeekViewset,\
    AddUserViewset

# Client
from client.views import SuggestionViewset, MessageNoticeViewset,AppLaunchImageCommonViewset, \
    AppLaunchImageLatestViewset, APPMessageNoticeViewset, JWMessageNoticeViewset, JWMessageNoticeGroupViewset, \
    APPMessageNoticeGroupViewset, JWMessageNoticePushViewset, APPMessageReadViewset, JWMessageReadViewset, \
    JWMessageOneNoticeViewset, APPMessageOneNoticeViewset, ErrorLogViewset, APPMessageNoticePushViewset

# PE
from pe.views import PeAccountTemViewset, PeAccountViewset, AttentanceNumViewset, GetAllPeAccountViewset, \
    DeletePeAccountTemViewset

# User Operation
from user_operation.views import PushSettingsViewset, UserLoginInfoViewset, UpdateStatisticsViewset

router = DefaultRouter()  # Visit the API list website
# router = SimpleRouter()  # Can not visit the API list website


# Client URLs

# User register
router.register(r'v1/register', UserRegViewset, base_name="register")

# User login
router.register(r'v1/login', LoginViewset, base_name="login")

# Send message code
router.register(r'v1/smsverifycode', SmsCodeViewset, base_name="sms_code")

# Check whether the TEL exists
router.register(r'v1/telcheck', TelInfoViewset, base_name="telcheck")

# Change password (Known Original Password)
router.register(r'v1/pwdwithraw', PasswordChangeWithKnowRawViewset, base_name="pwdwithraw")

# Change password (Forget Original Password, check ID with message code)
router.register(r'v1/pwdwithsms', PasswordChangeWithSmsViewset, base_name="pwdwithsms")

# Config about Message service
router.register(r'v1/smsswitch', SmsSwitchViewset, base_name="smsswitch")

# Check APP push messages
router.register(r'v1/clientmessage', MessageNoticeViewset, base_name="clientmessage")

# APP initial image (common)
router.register(r'v1/imagecommon', AppLaunchImageCommonViewset, base_name="imageCommon")

# APP initial image (latest)
router.register(r'v1/imagelatest', AppLaunchImageLatestViewset, base_name="imageLatest")

# User upload portrait
router.register(r'v1/userimage', UserImageViewset, base_name="userimage")

# User suggestion
router.register(r'v1/suggestion', SuggestionViewset, base_name="suggestion")


# Message Push URLs

# Check push message
router.register(r'v1/appmessagenotice', APPMessageNoticeViewset, base_name="APPMessageNotice")

# Push message about Student Affairs System (Group)
router.register(r'v1/jwpushmsg', JWMessageNoticeGroupViewset, base_name="JWMessageNoticeGroup")

# Push message about APP (Group)
router.register(r'v1/apppushmsg', APPMessageNoticeGroupViewset, base_name="APPMessageNoticeGroup")

# Push message about Student Affairs System (Individual)
router.register(r'v1/jwpushonemsg', JWMessageNoticePushViewset, base_name="JWMessageNoticePush")

# Push message about APP (Individual)
router.register(r'v1/apppushonemsg', APPMessageNoticePushViewset, base_name="APPMessageNoticePush")

# Modify the status of reading message (Student Affairs System)
router.register(r'v1/jwmsgreadstatus', JWMessageReadViewset, base_name="JWMessageReadStatus")

# Modify the status of reading message (APP)
router.register(r'v1/appmsgreadstatus', APPMessageReadViewset, base_name="APPMessageReadStatus")

# Get the latest one message (Student Affairs System)
router.register(r'v1/jwonemessagenotice', JWMessageOneNoticeViewset, base_name="JWMessageOneNotice")

# Get the latest one message (APP)
router.register(r'v1/apponemessagenotice', APPMessageOneNoticeViewset, base_name="APPMessageONeNotice")



# Student Dormitory URLs

# Check the electricity charge information
router.register(r'v1/electriccharge', ElectricChargeViewset, base_name="electriccharge")

# Temporary dormitory record
router.register(r'v1/dorminfotem', DormInfoTemViewset, base_name="dorminfotem")


# Student Information URLs

# Student grade
router.register(r'v1/grade', GradeViewset, base_name="grade")

# Student curriculum
router.register(r'v1/curriculum', CurriculumViewset, base_name="curriculum")

# Student attendance
router.register(r'v1/attendance', AttendanceViewset, base_name="attendance")

# Student class switch information
router.register(r'v1/classswitch', ClassSwitchViewset, base_name="classswitch")

# Student exam schedule
router.register(r'v1/exam', ExamViewset, base_name="exam")

# Query the times about error password
router.register(r'v1/loginerrornum', LoginErrorNumViewset, base_name="loginerrornum")

# Check user information
router.register(r'v1/userdetail', UserDetailViewset, base_name="userdetail")

# Check user Student Affairs System information status
router.register(r'v1/userjwstatus', UserJwStatusViewset, base_name="userjwstatus")

# Link account information of Student Affairs System
router.register(r'v1/userjwbind', UserJwBindViewset, base_name="userjwbind")

# Update Student Affairs System information
router.register(r'v1/userinfoupdate', UserinfoUpdateViewset, base_name="userinfoUpdate")

# Get Student Affairs System information 1
router.register(r'v1/userinfoquery1', UserinfoQuery1Viewset, base_name="userinfoquery1")

# Get Student Affairs System information 2
router.register(r'v1/userinfoquery2', UserinfoQuery2Viewset, base_name="userinfoquery2")

# Get Student Affairs System information 3
router.register(r'v1/userinfoquery3', UserinfoQuery3Viewset, base_name="userinfoquery3")

# Get Student Affairs System information 4
router.register(r'v1/userinfoquery4', UserinfoQuery4Viewset, base_name="userinfoquery4")

# Check Student Affairs System account status
router.register(r'v1/logininfocheck', UserLoginInfoCheckViewset, base_name="logininfoCheck")

# User PE lesson account (temporary)
router.register(r'v1/peaccounttem', PeAccountTemViewset, base_name="PeAccountTem")

# User PE lesson account
router.register(r'v1/peaccount', PeAccountViewset, base_name="PeAccount")

# Upload attendance information
router.register(r'v1/peattendance', AttentanceNumViewset, base_name="PeAttendance")

# Get JG Push User ID
router.register(r'v1/jgpushid', PushSettingsViewset, base_name="JgPushId")

# Get the latest week number
router.register(r'v1/currentweek', CurrentWeekViewset, base_name="currentWeek")

# Get Student Affairs System Message
router.register(r'v1/jwmessagenotice', JWMessageNoticeViewset, base_name="JWMessageNotice")

# Get all PE account information
router.register(r'v1/allpeaccount', GetAllPeAccountViewset, base_name="GetAllPeAccount")

# Get user login records
router.register(r'v1/userlogininfo', UserLoginInfoViewset, base_name="UserLoginInfo")

# Query dormitory account information
router.register(r'v1/querydormtem', DormInfoTemQueryViewset, base_name="DormInfoTemQuery")

# Add user account information (SYSTEM UPDATE)
router.register(r'v1/adduser', AddUserViewset, base_name="AddUser")

# Upload client error log
router.register(r'v1/errorlog', ErrorLogViewset, base_name="ErrorLog")

# Update statistics （Server）
router.register(r'v1/updatestatistics', UpdateStatisticsViewset, base_name="UpdateStatistics")


urlpatterns = [
    url(r'^admin/', xadmin.site.urls),

    # login for debug
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # drf api documentation
    url(r'^documentation/', include_docs_urls(title='Walking TKK API Documentation')),

    # 配置router的url
    url(r'^', include(router.urls)),

]
