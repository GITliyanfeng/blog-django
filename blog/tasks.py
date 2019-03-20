# -*- coding: utf-8 -*-
# @Time    : 2019/3/20 0020 17:46
# @Author  : __Yanfeng
# @Site    : 
# @File    : tasks.py
# @Software: PyCharm
from celery import shared_task
from datetime import date

from django.core.cache import cache
from django.db.models import F

from blog.models import Post


@shared_task
def handle_visited(path,uid, id):
    increase_pv = False
    increase_uv = False
    pv_key = f'pv:{uid}:{path}'
    uv_key = f'uv:{uid}:{str(date.today())}:{path}'
    if not cache.get(pv_key):
        increase_pv = True
        cache.set(pv_key, 1, 1 * 60)
    if not cache.get(uv_key):
        increase_uv = True
        cache.set(uv_key, 1, 24 * 60 * 60)

    if increase_pv and increase_uv:
        return Post.objects.filter(pk=id).update(pv=F('pv') + 1, uv=F('uv') + 1)
    elif increase_pv:
        return Post.objects.filter(pk=id).update(pv=F('pv') + 1)
    elif increase_uv:
        return Post.objects.filter(pk=id).update(uv=F('uv') + 1)
