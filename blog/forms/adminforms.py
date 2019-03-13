# -*- coding: utf-8 -*-
# @Time    : 2019/3/13 0013 19:07
# @Author  : __Yanfeng
# @Site    : 
# @File    : adminforms.py
# @Software: PyCharm
from django import forms

"""自定义django admin的form"""


class PostAdminForm(forms.ModelForm):
    # desc 字段以大文本框的形式显式
    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False)
