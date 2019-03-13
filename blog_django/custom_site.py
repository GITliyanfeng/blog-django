# -*- coding: utf-8 -*-
# @Time    : 2019/3/13 0013 19:27
# @Author  : __Yanfeng
# @Site    : 
# @File    : custom_site.py
# @Software: PyCharm
from django.contrib.admin import AdminSite


class CustomSite(AdminSite):
    site_header = 'Blog_Django'
    site_title = 'Blog后台管理系统'
    index_title = '管理系统首页'


custom_site = CustomSite(name='cus_admin')
