from django.contrib.auth.models import User
from django.db import models

class Link(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )
    title = models.CharField(max_length=50,verbose_name='标题')
    href = models.URLField(verbose_name='链接')
    status = models.PositiveIntegerField(default=STATUS_NORMAL,choices=STATUS_ITEMS,
                                     verbose_name='状态')
    weight = models.PositiveIntegerField(default=1,choices=zip(range(1,6),
                                            range(1,6)),verbose_name='权重',
                                         help_text='权重高的 排前面  ')
    owner = models.ForeignKey(User,verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    class Meta:
        verbose_name_plural =verbose_name = "友链"

class SideBar(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )
    SIDE_TYPE=(
        (1,'HTML'),
        (2,'最新文章'),
        (3,'最热文章'),
        (4,'最近评论'),
    )

    title = models.CharField(max_length=50,verbose_name="标题")
    display_type= models.PositiveIntegerField(default=1,choices=SIDE_TYPE,
                                                verbose_name='展示类型')
    content = models.CharField(max_length=500,blank=True,verbose_name='内容',
                                help_text='如果不是html ,可以为空')
    status = models.PositiveIntegerField(default=STATUS_NORMAL,choices=STATUS_ITEMS,verbose_name='状态')
    owner = models.ForeignKey(User, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name_plural = verbose_name = "侧边栏"