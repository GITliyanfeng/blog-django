# -*- coding: utf-8 -*-
# @Time    : 2019/3/19 0019 16:25
# @Author  : __Yanfeng
# @Site    : 
# @File    : search_indexes.py
# @Software: PyCharm
from haystack import indexes
from .models import Post


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        return self.get_model().latest_posts()
