from django.shortcuts import render
from django.http import HttpResponse

from blog.models import Tag, Post, Category
from config.models import SideBar


# Create your views here.

def post_list(request, category_id=None, tag_id=None):
    tag = None
    category = None
    if tag_id:
        post, tag = Post.get_by_tag(tag_id)
    elif category_id:
        post, category = Post.get_by_category(category_id)
    else:
        post = Post.latest_posts()
    ctx = {
        'category': category,
        'tag': tag,
        'post': post,
        'sidebars': SideBar.get_all()
    }
    ctx.update(Category.get_navs())
    return render(request, 'blog/list.html', ctx)


def post_detail(request, post_id):
    try:
        posts = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        posts = None
    ctx = {'post': posts, 'sidebars': SideBar.get_all()}
    ctx.update(Category.get_navs())
    return render(request, 'blog/detail.html', ctx)
