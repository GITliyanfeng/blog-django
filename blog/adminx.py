import xadmin
from xadmin import views
from xadmin.filters import manager
from xadmin.filters import RelatedFieldListFilter
from django.utils.html import format_html
from django.urls import reverse

from blog.models import Tag, Category, Post
from blog.forms.adminforms import PostAdminForm
from blog_django.base_admin import BaseOwnerAdmin
from xadmin.layout import Row, Fieldset, Container


# Register your models here.

class PostInline(object):  # admin.StackedInline 只是样式不同
    """内联数据管理---分类下面直接管理相对应的文章"""
    form_layout = (
        Container(
            Row('title', 'desc')
        )
    )
    extra = 0  # 控制额外多出几个
    model = Post


@xadmin.sites.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    inlines = (PostInline,)
    list_display = ('name', 'status', 'is_nav', 'post_count', 'created_time')
    fields = ('name', 'status', 'is_nav')

    def post_count(self, obj):
        print(obj)
        return obj.post_set.count()

    post_count.short_description = '文章数量'


@xadmin.sites.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')


@manager.register
class CategoryOwnerFilter(RelatedFieldListFilter):
    """自定义过滤器"""

    @classmethod
    def test(cls, field, request, params, model, admin_view, field_path):
        return field.name == 'category'

    def __init__(self, field, request, params, model, admin_view, field_path):
        super().__init__(field, request, params, model, admin_view, field_path)
        # 重新获取lookup_choices 根据 owner过滤,个人只能获取自己的数据
        self.lookup_choices = Category.objects.filter(owner=request.user).values_list('id', 'name')


@xadmin.sites.register(Post)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    list_display = [
        'title', 'category', 'status',
        'created_time', 'owner', 'operator'
    ]
    list_filter = ('category',)
    search_fields = ['title', 'category__name']
    actions_on_top = True
    """
    要求格式
    fieldsets = (
        ('名称',{
            '配置一':xxx,
            '配置二':xxx
        }),
        ('名称',{}),
    )
    配置项有:
    - description: 描述<string>
    - fields: 显式字段顺序<tuple>
    - classes: 当前块儿的样式 <tuple>  collapse 是单击展开可隐藏, wide 是常规显式
    """
    form_layout = (
        Fieldset('基础配置',
                 Row('title', 'category'),
                 'status',
                 'tag',
                 'is_markdown',
                 ),
        Fieldset('内容',
                 'desc',
                 'content_ck',
                 'content_md',
                 'content',
                 ),
    )

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>', reverse('xadmin:blog_post_change', args=(obj.id,))
        )

    operator.short_description = '操作'

    @property
    def media(self):
        """在Media信息中可以自定义静态资源的引入"""
        # xadmin 导入静态文件
        media = super().media
        media.add_js([])
        media.add_css({'all': []})
        return media


# 后台系统名称页脚设置、设置后台菜单为收缩样式
class GlobalSetting(object):
    site_title = 'LeeBlog后台管理'
    site_footer = 'LeeBlog.com'
    # menu_style = 'accordion'


# 配置后台主题
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = False


xadmin.site.register(views.CommAdminView, GlobalSetting)
xadmin.site.register(views.BaseAdminView, BaseSetting)
