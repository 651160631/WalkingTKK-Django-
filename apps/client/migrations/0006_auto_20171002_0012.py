# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-02 00:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0005_auto_20171002_0010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suggestion',
            name='image_1_url',
            field=models.TextField(null=True),
        ),
    ]
