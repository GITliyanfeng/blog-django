目录结构
---

一个项目的目录结构通常是

```shell
-project
   |- LICENSE
   |- MANIFEST.in
   |- Readme.md
   |- conf
   |- src
   |- requirements.txt
   |- setup.py
   |- others
   |- .gitignore
   |- fabfile
```

Django的目录结构应该分离为

```shell
-project
   \-app1
   \-app2
   \-project
      \-settings
         \-__init__.py
         \-base.py
         \-develop.py
         \-product.py
      \-manage.py
```

基本后台步骤:

+ 分离settings
+ 创建app
+ 构建model层
+ 配置Admin
+ 开启LogEntry

基本前台步骤:

+ 分析页面
    + 博客首页: https://localhost:8080/
    + 博文详情页: https://localhost:8080/post/<post_id>.html
    + 分类列表页:https://localhost:8080/category/<category_id>/
    + 标签列表页:https://localhost:8080/tag/<tag_id>/
    + 友链展示页::https://localhost:8080/links/
    
+ 划分View逻辑
    + 根据不同的查询条件展示列表页面
    + 展示博文详情页
    + 单独处理友链的View
    
    1. 列表页View 根据不同的查询条件分别展示,博客首页,分开类列表页,标签列表页
    1. 文章页View 展示博文详情页面
    1. 友链View   展示所有友情链接
    
构建要点:

+ 视图函数中不要过多的逻辑,视图函数的主要功能是将数据渲染到页面,处理数据的功能放到model层面
    + 例如: posts_list函数在主页面,category页面,tag页面都用到了,一般的方式是通过同一视图函数
    中定义复杂的分支结构,在视图函数中处理并且过滤数据,这样会让人感到这个函数很庞大,不舒服,我们可以
    通过在model层定义相应的静态方法或者类方法,来使视图函数部分`变瘦`,将来进行维护视图的时候一目了然
+ templates中将公共代码抽取,通过继承的方式,而不是简单的赋值粘贴,方便后期维护
+ 对具有相同结构<不同数据类型>的页面部分进行封装
    + 例如:sidebar部分,可以显示 最新文章 , 最热文章 , 最新评论等,他们的结构的是一致的,可以进行封装
    ,在model层定义property方法,直接根据不同的数据类型进行渲染,返回渲染后的数据,在页面中直接使用sidebar
    实例对象调用,减少在页面中,视图函数中的分支结构判断
    
    
FBV CBV?

- 选择视图函数  还是类视图? 无高低之分.针对不同场景的适用性,合理选择


理解 函数 和 类?

- 如果代码重复使用,同时具有共享的数据,这个时候考虑封装成一个类 --<类的继承复用>

class-base-view?

> View是一个接受request返回response的对象,允许结构化View以及通过继承或者Mixin的方式复用

django提过的class-base-view 的使用场景和优缺点?

1. View 基础View,实现HTTP的dispatch,GET请求调用get方法,POST请求调用post方法,但是自己没有实现相应的方法
1. TemplateView 继承自View,可以解析模板,实现get方法,可以传递变量到模板中渲染
1. DetailView 继承自View,实现get,可绑定某一个模板,用来获取单个实例的数据
1. ListView 继承自View,实现get,绑定某个模板,批量获取数据

```python
from django.http import HttpResponse

def index(request):
    if request.method == 'GET':
        return HttpResponse('index')

```
```python
from django.http import HttpResponse
from django.views import View

class indexView(View):
    def get(self,request):
        return HttpResponse('index')

```

体现开-闭原则,当有新的请求方式的时候,使用View方式,不用去修改原来的业务代码<比如添加分支结构>
而是,增加一个方法<例如增加一个post方法来处理post请求>


CBV FBV 对请求处理的差别在哪里？

HTTP请求 --> Django -[转化]-> request(instance) --[middleware-process_request]--> 解析URL -->
根据URL和View的映射 --[传递request对象]-->View(function-view or class-base-view)

这就是为什么function-view 在定义的时候第一个参数是request，因为通过映射传递了过来，他对request的处理流程
就是函数流程，函数怎么写，他就怎么处理，最后返回response对象

class-base-view的处理流程：
 
 classview通过对外暴露的接口as_view()方法来处理请求
 
 通过源码可以看到它其实返回的是一个闭包，这个闭包在Django解析完请求后调用，闭包内部的处理是：
 
 + 给class<定义的xxxView>传递参数 request，args，kwargs
 + 根据请求的方式调用class.post 或者 class.get 方法
    + 首先调用dispatch 分发
    + 调用请求方法
        + GET 会通过get_queryset方法获取数据
        + get_context_data 中组装哪些数据会在模板中被渲染
            + 其中，首先调用get_paginate_by 拿到每一页的数据 <如果是获取序列数据的话>
            + 调用get_content_object_by_name 拿到要渲染到模板的queryset的名字
            + 调用paginate_queryset进行分页处理
        + 调用render_to_response数据渲染到模板
            + 调用get_template_names拿到模板
            + 传递request,context,template_name渲染到模板
            
            
            
完整的Blog除了上面的内容显示外,还需要具备的

+ search
    + 过滤数据源 页面依然使用list页面,依然继承IndexView
+ comment  
    + Javascript异步提交
    + 单页面提交
    + 当前页面提交
    
    
 + markdown 格式支持
 
 
 + 访问统计
 
 访问统计方式通常有?
 
 1. 基于当此访问后端实时处理
 1. 基于当此访问后端延时处理--Celery(分布式任务队列)
 1. 前端通过JavaScript埋点,或者img标签来统计
 1. 基于Nginx的日志分析来统计
 
 方式一其实是在获取文章详情的时候 对当前文章的访问量PV UV进行+1的操作
 
 ```python
from django.db.models import Q, F
from blog.views import CommonViewMixin,DetailView

class PostDetailView(CommonViewMixin, DetailView):
    # 省略其他代码
    def get(self,request,*args,**kwargs):
    response = super(PostDetailView, self).(request,*args,**kwargs)
    Post.objects.filter(pk=self.object.id).update(pv=F('pv')+1,uv=F('uv')+1)
```
存在的缺点是,每一个访问都会引起数据库的写的操作,性能差

所以引入了异步化的思想<让一个第三方的工具去执行这项任务>Celery

第三种和第四种是常用的方式,应因为访问量巨大,不可能在业务代码中实现.需要一个独立出来的系统去做统计,麻烦在统计数据和业务分离.
业务需要数据作展示,统计i同需要拿业务系统的数据做分析

无论哪种统计都需要解决恶意刷新的问题,如何区分用户?
+ 用户IP和浏览器类型生成的MD5
+ 系统生成的唯一id放到cookies中
+ 用户登陆?

方式一  用户重合 ,同浏览器,同一个出口IP
方式二  换浏览器?
方式三  没人会登陆之后才能看文章,实施难度大

选择方式二,用户访问的时候记录用户的访问数据,这些数据应该被放在缓存中,临时数据,有过期时间

需要考虑:
+ id如何生成
    + 使用uuid库
+ 那一步给有用户配置id
    + 使用middleware来标记
+ 用什么样子的缓存
    + django缓存接口
    
    

合理的系统是  分离统计 避免用户在访问的时候执行数据库的写的操作   
    
 