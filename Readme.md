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