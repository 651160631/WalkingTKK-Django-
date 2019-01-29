# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-12 10:00
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('client', '0009_applaunchimagecommon_applaunchimagelatest'),
    ]

    operations = [
        migrations.CreateModel(
            name='APPMessageNotice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='NULL', max_length=100, verbose_name='通知标题')),
                ('content', models.CharField(default='NULL', max_length=300, verbose_name='通知内容')),
                ('all_student', models.BooleanField(default=False, verbose_name='通知所有人')),
                ('grade', models.CharField(default='NULL', max_length=30, null=True, verbose_name='用户年级')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '通知用户关于APP的消息',
                'verbose_name_plural': '通知用户关于APP的消息',
            },
        ),
        migrations.CreateModel(
            name='JWMessageNotice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='NULL', max_length=100, verbose_name='通知标题')),
                ('content', models.CharField(default='NULL', max_length=300, verbose_name='通知内容')),
                ('all_student', models.BooleanField(default=False, verbose_name='通知所有人')),
                ('grade', models.CharField(default='NULL', max_length=30, null=True, verbose_name='用户年级')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '通知用户关于教务系统的消息',
                'verbose_name_plural': '通知用户关于教务系统的消息',
            },
        ),
    ]
