# -*- coding: utf-8 -*-
# @Time    : 2019/3/13 0013 19:07
# @Author  : __Yanfeng
# @Site    : 
# @File    : adminforms.py
# @Software: PyCharm
from dal import autocomplete
from django import forms
from blog.models import Category, Tag, Post

"""自定义django admin的form"""


class PostAdminForm(forms.ModelForm):
    # desc 字段以大文本框的形式显式
    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False)
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=autocomplete.ModelSelect2(url='categoryAutocompete'),
        label='分类',
    )
    tag = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url='tagAutocomplele'),
        label='标签',
    )

    class Meta:
        model = Post
        fields = ('category', 'tag', 'title', 'desc', 'content', 'status')
