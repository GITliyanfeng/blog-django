# -*- coding: utf-8 -*-
# @Time    : 2019/3/15 0015 18:55
# @Author  : __Yanfeng
# @Site    : 
# @File    : sitemap.py
# @Software: PyCharm
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from blog.models import Post


class PostSiteMap(Sitemap):
    changefreq = 'always'
    priority = 1.0
    protocol = 'https'

    def items(self):
        return Post.objects.filter(status=Post.STATUS_NORMAL)

    def lastmod(self, obj):
        return obj.created_time

    def location(self, obj):
        return reverse('postDetail', args=(obj.pk,))
