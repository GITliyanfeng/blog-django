import xadmin
from comment.models import Comment


# Register your models here.

@xadmin.sites.register(Comment)
class CommentAdmin(object):
    list_display = ['target', 'nickname', 'content', 'website', 'created_time']
