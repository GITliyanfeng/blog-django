from django.contrib.auth.models import User
from django.db import models
import mistune


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

    def __str__(self):
        return self.name

    @classmethod
    def get_navs(cls):
        categories = Category.objects.filter(status=cls.STATUS_NORMAL)
        nav_categories = []
        normal_categories = []
        # 循环相当于只执行了上面一次对数据库的查询
        for cate in categories:
            if cate.is_nav:
                nav_categories.append(cate)
            else:
                normal_categories.append(cate)
        # nav_categories = categories.filter(is_nav=True)   每一个都会有一个I/O
        # normal_categories = categories.filter(is_nav=False)
        return {
            'navs': nav_categories,
            'categories': normal_categories
        }

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

    def __str__(self):
        return self.name

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
    # pv和uv来分别统计每篇文章的访问量
    pv = models.PositiveIntegerField(default=1)
    uv = models.PositiveIntegerField(default=1)
    title = models.CharField(max_length=255, verbose_name='标题')
    desc = models.CharField(max_length=1024, blank=True, verbose_name='摘要')
    content = models.TextField(verbose_name='正文MarkDown格式', help_text="正文必须为MarkDown格式")
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name='状态',
                                         db_column='pstatus')
    # 多对一  多个文章对应一个category
    category = models.ForeignKey(Category, verbose_name='分类')
    # 多对多关系 一个文章多个标签,多个标签可以对应一个文章
    tag = models.ManyToManyField(Tag, verbose_name='标签')
    owner = models.ForeignKey(User, verbose_name='作者')
    body = models.TextField(verbose_name='正文 HTML格式', blank=True, editable=False)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', db_index=True)

    def __str__(self):
        return self.title

    @staticmethod
    def get_by_tag(tag_id):
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            tag = None
            post = []
        else:
            post = tag.post_set.filter(status=Post.STATUS_NORMAL).select_related('owner', 'category')
        return post, tag

    @staticmethod
    def get_by_category(category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category = None
            post = []
        else:
            post = category.post_set.filter(status=Post.STATUS_NORMAL).select_related('owner', 'category')
        return post, category

    @classmethod
    def latest_posts(cls):
        queryset = cls.objects.filter(status=cls.STATUS_NORMAL)
        return queryset

    @classmethod
    def hot_posts(cls):
        """获取高点击连量的文章"""
        return cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-pv')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        """重写save方法,需要将markdown格式代码转换成分Html"""
        self.body = mistune.markdown(self.content)
        super(Post, self).save(force_insert=False, force_update=False, using=None,
                               update_fields=None)

    class Meta:
        db_table = 'blog_posts'
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-id']
