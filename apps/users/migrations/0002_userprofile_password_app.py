# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-28 16:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='password_app',
            field=models.CharField(default='NULL', max_length=20, verbose_name='用户APP的登录密码'),
        ),
    ]
