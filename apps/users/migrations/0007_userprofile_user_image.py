# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-02 11:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20171001_2114'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='user_image',
            field=models.CharField(default='NULL', max_length=500, verbose_name='用户头像链接'),
        ),
    ]
