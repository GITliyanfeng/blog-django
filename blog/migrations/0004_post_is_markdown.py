# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-03-15 16:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20190315_0019'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_markdown',
            field=models.BooleanField(default=False, verbose_name='MarkDown语法'),
        ),
    ]
