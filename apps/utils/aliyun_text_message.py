#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import json
import os
import sys

import requests

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd+"../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "walkingTKK.settings")

import django
django.setup()

from user_operation.models import TextMessage

class Aliyun(object):
    def __init__(self):
        self.appcode = '3ed8ac140fae4798b9fd1bd77000000000'
        self.url = "http://sms.market.alicloudapi.com/singleSendSms"

    def send_sms(self, mobile, ParamString, SignName, TemplateCode):
        RecNum = mobile
        querys = 'ParamString=' + ParamString + '&RecNum=' + RecNum + '&SignName=' + SignName + '&TemplateCode=' + TemplateCode
        url = self.url + '?' + querys
        headers = {
            'Authorization': 'APPCODE ' + self.appcode
        }
        response = requests.get(url, headers=headers)
        content = response.text
        re_dict = json.loads(content)
        # 保存发送记录
        message_record = TextMessage()
        message_record.content = str(url)
        message_record.tel = mobile
        message_record.save()
        return re_dict


if __name__ == "__main__":
    aliyun = Aliyun()
    aliyun.send_sms("13057117720", "{'code':'0000'}", "行走嘉园", "SMS_69205776")
