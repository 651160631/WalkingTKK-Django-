# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-08 09:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20171008_0949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='password_jw',
            field=models.TextField(default='NULL', verbose_name='教务系统密码'),
        ),
    ]
