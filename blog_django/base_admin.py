# -*- coding: utf-8 -*-
# @Time    : 2019/3/13 0013 20:18
# @Author  : __Yanfeng
# @Site    : 
# @File    : base_admin.py
# @Software: PyCharm
from django.contrib import admin


class BaseOwnerAdmin(admin.ModelAdmin):
    """
    抽取admin基类,将具有相同逻辑的代码都放在一起
    1. 用来自动补充文章,分类,标签,侧边栏,友链的model的owner字段
    2. 用于针对当前用户 过滤当前用户的数据
    """
    exclude = ('owner',)

    def get_queryset(self, request):
        qs = super(BaseOwnerAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(BaseOwnerAdmin, self).save_model(request, obj, form, change)
