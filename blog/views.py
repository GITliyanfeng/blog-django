from django.views.generic import DetailView, ListView
from django.shortcuts import get_object_or_404
from blog.models import Tag, Post, Category
from config.models import SideBar


# Create your views here.

class CommonViewMixin:
    """定义commonMixin来处理公用数据"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': SideBar.get_all()
        })
        context.update(Category.get_navs())
        return context


class IndexView(CommonViewMixin, ListView):
    """indexView 获取所有数据"""
    queryset = Post.latest_posts()
    paginate_by = 1  # 自带分页功能 这里是每一页 显示的条数
    context_object_name = 'post'  # 在页面中使用的变量 默认是object_list
    template_name = 'blog/list.html'


class CategoryView(IndexView):
    """categoryView根据传入的category_id过滤数据"""

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category': category
        })
        return context

    def get_queryset(self):
        """从写get——queryset，因为要根据分类过滤"""
        queryset = super(CategoryView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)


class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super(TagView, self).get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag
        })
        return context

    def get_queryset(self):
        queryset = super(TagView, self).get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag__id=tag_id)


class PostDetailView(CommonViewMixin,DetailView):
    queryset = Post.latest_posts()
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    # 定义获取当条数据传入的参数
    pk_url_kwarg = 'post_id'
