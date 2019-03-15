# -*- coding: utf-8 -*-
# @Time    : 2019/3/15 0015 21:19
# @Author  : __Yanfeng
# @Site    : 
# @File    : autocomplete.py
# @Software: PyCharm
from dal import autocomplete
from blog.models import Category, Tag


class CategoryAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Category.objects.none()
        qs = Category.objects.filter(owner=self.request.user)
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class TagAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Tag.objects.none()
        qs = Tag.objects.filter(owner=self.request.user)
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs
