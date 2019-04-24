import xadmin
from django.contrib import admin
from .models import Comment
# Register your models here.

class CommentAdmin(object):
    list_display = ('target', 'nickname', 'content', 'website', 'created_time')

xadmin.site.register(Comment, CommentAdmin)