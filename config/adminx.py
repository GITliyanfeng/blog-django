import xadmin
from xadmin.layout import Fieldset
from blog_django.base_admin import BaseOwnerAdmin
from config.models import Link, SideBar


# Register your models here.

@xadmin.sites.register(Link)
class LinkAdmin(BaseOwnerAdmin):
    list_display = ['title', 'href', 'status', 'weight', 'created_time']
    form_layout = Fieldset('友链', 'title', 'href', 'status', 'weight')


@xadmin.sites.register(SideBar)
class SideBarAdmin(BaseOwnerAdmin):
    list_display = ('title', 'display_type', 'content', 'created_time')
    form_layout = Fieldset('侧边栏', 'title', 'display_type', 'content')
