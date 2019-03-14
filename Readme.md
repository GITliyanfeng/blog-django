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