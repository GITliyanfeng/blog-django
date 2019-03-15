# -*- coding: utf-8 -*-
# @Time    : 2019/3/14 0014 23:41
# @Author  : __Yanfeng
# @Site    : 
# @File    : comment_tag.py
# @Software: PyCharm
from django import template
from comment.forms import CommentForm
from comment.models import Comment

register = template.Library()


@register.inclusion_tag('comment/block.html')
def comment_block(target):
    return {
        'target': target,
        'comment_form': CommentForm(),
        'comment_list': Comment.get_by_target(target=target)
    }
