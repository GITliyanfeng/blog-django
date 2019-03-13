from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from blog.models import Tag, Category, Post
from blog.forms.adminforms import PostAdminForm


# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'is_nav', 'post_count', 'created_time')
    fields = ('name', 'status', 'is_nav')

    def post_count(self, obj):
        print(obj)
        return obj.post_set.count()

    post_count.short_description = '文章数量'

    # 在使用django的admin保存数据的时候触发的方法
    def save_model(self, request, obj, form, change):
        obj.owner = request.user  # 将当前登陆用户创建为作者
        return super(CategoryAdmin, self).save_model(request, obj, form, change)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user  # 将当前登陆用户创建为作者
        return super(TagAdmin, self).save_model(request, obj, form, change)


class CategoryOwnerFilter(admin.SimpleListFilter):
    """自定义过滤器"""
    title = '个人分类过滤'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        """查询操作"""
        # 查询当前登陆用户的所有分类,返回的是[id,name]name用于在过滤器中展示 id 用于向下传递
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        """输出向列表页面的数据"""
        category_id = self.value()
        # self.value()方法可以接收lookups方法中传递的值id,这个id是Category的id
        if category_id:
            return queryset.filter(category_id=category_id)
        return queryset


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = [
        'title', 'category', 'status',
        'created_time', 'owner', 'operator'
    ]
    list_filter = [CategoryOwnerFilter]
    search_fields = ['title', 'category__name']
    actions_on_top = True
    actions_on_bottom = True

    # 编辑页面
    # save_on_top = True # 保存 编辑按钮是否在顶部显式
    # fields配置编辑页面字段的显式顺序
    # fields = (
    #     ('category', 'title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag'
    # )
    # fieldsets配置编辑页面的布局
    # filter_horizontal = ('tag',)  # 多对多字段展示效果一 左侧栏目选中 --> 右侧
    filter_vertical = ('tag',)  # 多对多字段效果二  上侧栏目选中 --> 下侧
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
    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (
                ('title', 'category'),
                'status'
            )
        }),
        ('内容', {
            'fields': (
                'desc',
                'content'
            )
        }),
        ('额外信息', {
            'classes': ('collapse',),
            'fields': ('tag',)
        })
    )

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>', reverse('admin:blog_post_change', args=(obj.id,))
        )

    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        """定义列表页只能获取自己的文章"""
        qs = super(PostAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)

    class Media:
        """在Media信息中可以自定义静态资源的引入"""
        css = {
            # 导入css
            # 'all': ('https://cdn.bootcss.com/twitter-bootstrap/4.3.1/css/bootstrap.min.css',)
        }
        # 导入js
        js = ('https://cdn.bootcss.com/twitter-bootstrap/4.3.1/js/bootstrap.bundle.min.js',)
