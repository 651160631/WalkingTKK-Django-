# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-01 22:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_auto_20170929_2109'),
    ]

    operations = [
        migrations.AddField(
            model_name='suggestion',
            name='image_1',
            field=models.ImageField(null=True, upload_to='suggestion'),
        ),
    ]
