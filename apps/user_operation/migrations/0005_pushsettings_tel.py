# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-22 12:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_operation', '0004_pushsettings'),
    ]

    operations = [
        migrations.AddField(
            model_name='pushsettings',
            name='tel',
            field=models.CharField(default='NULL', help_text='和username保持一致', max_length=11, verbose_name='电话'),
        ),
    ]
