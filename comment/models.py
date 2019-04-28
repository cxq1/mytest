from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from blog.models import Post
# Create your models here.

class Comment(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )
    content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')
    
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    #target = models.ForeignKey(Post,verbose_name='评论目标',on_delete=models.CASCADE)
    content = models.CharField(max_length=2000,verbose_name='内容')
    nickname = models.CharField(max_length=20,verbose_name='匿名')
    website = models.URLField(verbose_name="网站")
    email = models.EmailField(verbose_name="邮箱")
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name='状态')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    class Meta:
        verbose_name_plural = verbose_name = "评论"

    @classmethod
    def get_comments(cls,content_type,object_id):
        return cls.objects.filter(content_type=content_type,object_id=object_id)