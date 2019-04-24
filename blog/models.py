import mistune
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.utils.functional import cached_property


class Category(models.Model):
    STATUS_NORMAL=1
    STATUS_DELETE=0
    STATUS_ITEMS=(
        (STATUS_NORMAL,'正常'),
        (STATUS_DELETE,'删除'),
    )
    name= models.CharField(max_length=50,verbose_name='名称')
    status=models.PositiveIntegerField(default=STATUS_NORMAL,
        choices=STATUS_ITEMS,verbose_name='状态')
    is_nav = models.BooleanField(default=False,verbose_name='是否为导航')
    owner = models.ForeignKey(User,verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural='分类'
    def __str__(self):
        return self.name

    @classmethod
    def get_nvas(cls):
        categories = cls.objects.filter(status=cls.STATUS_NORMAL)
        nav_categories=[]
        normal_cateogries=[]
        for cate in categories:
            if cate.is_nav:
                nav_categories.append(cate)
            else:
                normal_cateogries.append(cate)

        return {
            'navs':nav_categories,
            'categories':normal_cateogries,
        }


class Tag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )
    name=models.CharField(max_length=50,verbose_name='名称')
    status= models.PositiveIntegerField(default=STATUS_NORMAL,
        choices=STATUS_ITEMS,verbose_name='状态')
    owner = models.ForeignKey(User,verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    class Meta:
        verbose_name_plural = verbose_name = '标签'
    def __str__(self):
        return self.name



class Post(models.Model):
    STATUS_NORMAL=1
    STATUS_DELETE=0
    STATUS_ITEMS=(
        (STATUS_NORMAL,'正常'),
        (STATUS_DELETE,'删除'),
    )

    title = models.CharField(max_length=255,verbose_name='标题')
    desc = models.CharField(max_length=1024,blank=True,verbose_name='摘要')
    content = models.TextField(verbose_name='正文',help_text='正文必须为markdown格式')
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
        choices=STATUS_ITEMS,verbose_name='状态')
    category = models.ForeignKey(Category,verbose_name='分类')
    tag = models.ManyToManyField(Tag,verbose_name='标签')
    owner = models.ForeignKey(User,verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    content_html = models.TextField(verbose_name='正文HTML代码',blank=True,editable=True)
    is_md = models.BooleanField(default=False,verbose_name='markdown语法')

    @cached_property
    def tags(self):
        return ','.join(self.tag.values_list('name',flat=True))

    def save(self,*args,**kwargs):
        if self.is_md:
            self.content_html = mistune.markdown(self.content)
        else:
            self.content_html = self.content
        super().save(*args,**kwargs)

    pv = models.PositiveIntegerField(default=1)
    uv = models.PositiveIntegerField(default=1)
    @classmethod
    def hot_pots(cls):
        return cls.objects.filter(status=Post.STATUS_NORMAL).order_by('-pv')

    class Meta:
        verbose_name_plural = verbose_name = '文章'
        ordering=['-id']
    def __str__(self):
        return self.title

    @staticmethod
    def get_by_tag(tag_id):
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            tag=None
            post_list=[]
        else:
            post_list= tag.post_set.filter(status=Post.STATUS_NORMAL)\
                .select_related('owner','category')
        return post_list,tag

    @staticmethod
    def get_by_category(category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category = None
            post_list=[]
        else:
            post_list = category.post_set.filter(status=Post.STATUS_NORMAL)\
                .select_related('owner','category')
        return category,post_list

    @classmethod
    def latest_post(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL)
