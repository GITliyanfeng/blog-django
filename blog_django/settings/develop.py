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
XADMIN_TITLE = 'Lee-Blog后台系统'
XADMIN_FOOTER_TITLE = 'power by lee'
