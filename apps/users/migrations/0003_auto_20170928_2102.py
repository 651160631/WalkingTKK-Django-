# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-28 21:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userprofile_password_app'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='error_num_app',
            field=models.IntegerField(default=0, verbose_name='客户端登录错误次数'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='error_num_jw',
            field=models.IntegerField(default=0, verbose_name='教务系统登录错误次数'),
        ),
    ]
