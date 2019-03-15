# -*- coding: utf-8 -*-
# @Time    : 2019/3/15 0015 18:08
# @Author  : __Yanfeng
# @Site    : 
# @File    : rss.py
# @Software: PyCharm
from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Rss201rev2Feed
from blog.models import Post


class ExtendedRSSFeed(Rss201rev2Feed):
    def add_item_elements(self, handler, item):
        super(ExtendedRSSFeed, self).add_item_elements(handler, item)
        handler.addQuickElement('content:html', item['content_html'])


class LatestPostFeed(Feed):
    feed_type = Rss201rev2Feed
    title = 'Lee blog system'
    link = '/rss/'
    description = 'Lee is a blog system power by django'

    def items(self):
        return Post.objects.filter(status=Post.STATUS_NORMAL)[:2]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.desc

    def item_link(self, item):
        return reverse('postDetail', args=(item.pk,))

    def item_extra_kwargs(self, item):
        return {'content_html': self.item_content_html(item)}

    def item_content_html(self, item):
        return item.body
