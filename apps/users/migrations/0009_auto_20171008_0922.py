# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-08 09:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20171002_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='password_app',
            field=models.CharField(default='NULL', max_length=200, verbose_name='用户APP的登录密码'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='password_jw',
            field=models.CharField(default='NULL', max_length=200, verbose_name='教务系统密码'),
        ),
    ]
