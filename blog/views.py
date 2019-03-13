from django.shortcuts import render
from django.http import HttpResponse

from blog.models import Tag, Post, Category


# Create your views here.

def post_list(request, category_id=None, tag_id=None):
    if tag_id:
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            posts = []
        else:
            posts = tag.post_set.filter(status=Post.STATUS_NORMAL)
    else:
        posts = Post.objects.filter(status=Post.STATUS_NORMAL)
        if category_id:
            posts = posts.filter(category_id=category_id)
    return render(request, 'blog/list.html', context={'posts': posts})


def post_detail(request, post_id):
    try:
        posts = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        posts = None
    ctx = {'posts': posts}
    return render(request, 'blog/detail.html', ctx)
