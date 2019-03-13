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