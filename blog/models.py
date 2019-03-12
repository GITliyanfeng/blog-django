from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Category(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )
    name = models.CharField(max_length=50, db_column='cname', verbose_name='名称')
    status = models.PositiveIntegerField(default=STATUS_NORMAL, db_column='cstatus', choices=STATUS_ITEMS,
                                         verbose_name='状态')
    is_nav = models.BooleanField(default=False, db_column='cis_nav', verbose_name='是否为导航')
    # 多对一关系
    owner = models.ForeignKey(User, db_column='cowner', verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, db_index=True, db_column='ccreated_time',
                                        verbose_name='创建时间')

    class Meta:
        db_table = 'blog_categories'
        verbose_name = '分类'
        verbose_name_plural = verbose_name


class Tag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )
    name = models.CharField(max_length=50, db_column='tname', verbose_name='名称')
    status = models.PositiveIntegerField(default=STATUS_NORMAL, db_column='tstatus', choices=STATUS_ITEMS,
                                         verbose_name='状态')
    # 多对一关系
    owner = models.ForeignKey(User, db_column='towner', verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, db_index=True, db_column='tcreated_time',
                                        verbose_name='创建时间')

    class Meta:
        db_table = 'blog_tags'
        verbose_name = '标签'
        verbose_name_plural = verbose_name


class Post(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '草稿'),
    )
    title = models.CharField(max_length=255, verbose_name='标题')
    desc = models.CharField(max_length=1024, blank=True, verbose_name='摘要')
    content = models.TextField(verbose_name='正文', help_text="正文必须为MarkDown格式")
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name='状态',
                                         db_column='pstatus')
    # 多对一  多个文章对应一个category
    category = models.ForeignKey(Category, verbose_name='分类')
    # 多对多关系 一个文章多个标签,多个标签可以对应一个文章
    tag = models.ManyToManyField(Tag, verbose_name='标签')
    owner = models.ForeignKey(User, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', db_index=True)

    class Meta:
        db_table = 'blog_posts'
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-id']
