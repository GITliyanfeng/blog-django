# -*- coding: utf-8 -*-
# @Time    : 2019/3/12 0012 23:22
# @Author  : __Yanfeng
# @Site    : 
# @File    : develop.py
# @Software: PyCharm

from .base import *  # NOQA

# dbug
DEBUG = True

# 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'blog.whoosh_cn_backend.WhooshEngine',
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    },
}
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 1
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

CELERY_BROKER_URL = 'redis://127.0.0.1/2'

CELERY_RESULT_BACKEND = 'django-db'
