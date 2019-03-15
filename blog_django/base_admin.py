# -*- coding: utf-8 -*-
# @Time    : 2019/3/13 0013 20:18
# @Author  : __Yanfeng
# @Site    : 
# @File    : base_admin.py
# @Software: PyCharm


class BaseOwnerAdmin(object):
    """
    抽取admin基类,将具有相同逻辑的代码都放在一起
    1. 用来自动补充文章,分类,标签,侧边栏,友链的model的owner字段
    2. 用于针对当前用户 过滤当前用户的数据
    """
    exclude = ('owner',)

    def get_list_queryset(self):
        qs = super(BaseOwnerAdmin, self).get_list_queryset()
        return qs.filter(owner=self.request.user)

    def save_models(self):
        self.new_obj.owner = self.request.user
        return super(BaseOwnerAdmin, self).save_models()
