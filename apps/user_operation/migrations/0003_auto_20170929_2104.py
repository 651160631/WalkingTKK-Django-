# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-29 21:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_operation', '0002_auto_20170928_1355'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MessageNotice',
        ),
        migrations.RemoveField(
            model_name='suggestion',
            name='user',
        ),
        migrations.DeleteModel(
            name='Suggestion',
        ),
    ]
