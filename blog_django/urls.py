"""blog_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from blog.views import PostDetailView, IndexView, CategoryView, TagView, SearchView, AuthorView
from config.views import LinkListView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^category/(?P<category_id>\d+)/$', CategoryView.as_view(), name='postListcate'),
    url(r'^tag/(?P<tag_id>\d+)/$', TagView.as_view(), name='postListtag'),
    url(r'^author/(?P<author_id>\d+)/$', AuthorView.as_view(), name='postListauthor'),
    url(r'^post/(?P<post_id>\d+).html$', PostDetailView.as_view(), name='postDetail'),
    url(r'^admin/', admin.site.urls),
    url(r'^search/$', SearchView.as_view(), name='search'),
    url(r'^links/$', LinkListView.as_view(), name='links'),
]
