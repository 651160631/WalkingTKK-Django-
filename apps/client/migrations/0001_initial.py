# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-29 21:04
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageNotice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(default='NULL', max_length=300, verbose_name='通知内容')),
                ('ios_version', models.CharField(default='NULL', max_length=100, null=True, verbose_name='iOS需要通知的版本')),
                ('andriod_version', models.CharField(default='NULL', max_length=100, null=True, verbose_name='Andriod需要通知的版本')),
                ('mina_version', models.CharField(default='NULL', max_length=100, null=True, verbose_name='小程序需要通知的版本')),
                ('grade', models.CharField(default='NULL', max_length=30, null=True, verbose_name='用户年级')),
                ('add_time', models.DateTimeField(auto_now=True, null=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '通知用户的最新消息',
                'verbose_name_plural': '通知用户的最新消息',
            },
        ),
        migrations.CreateModel(
            name='Suggestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=300, verbose_name='建议内容')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '用户建议',
                'verbose_name_plural': '用户建议',
            },
        ),
    ]
