# -*- coding: utf-8 -*-
# @Time    : 2019/3/20 0020 17:42
# @Author  : __Yanfeng
# @Site    : 
# @File    : celery.py
# @Software: PyCharm
from __future__ import absolute_import, unicode_literals
from celery import Celery
import os

PROFILE = os.environ.get('DJANGO_SELFBLOG_PROFILE', 'develop')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_django.settings.%s'%PROFILE)

app = Celery('blog_diango')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request:{0!r}'.format(self.request))
