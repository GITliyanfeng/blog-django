from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from blog.models import Tag, Category, Post


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


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category', 'status',
        'created_time', 'operator'
    ]
    list_display_links = []
    search_fields = ['title', 'category__name']
    actions_on_top = True
    actions_on_bottom = True

    # 编辑页面
    # save_on_top = True # 保存 编辑按钮是否在顶部显式
    fields = (
        ('category', 'title'),
        'desc',
        'status',
        'content',
        'tag'
    )

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>', reverse('admin:blog_post_change', args=(obj.id,))
        )

    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)
