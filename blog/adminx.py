import xadmin
from django.contrib.admin.models import LogEntry
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from xadmin.filters import manager,RelatedFieldListFilter
from xadmin.layout import Fieldset, Row,Container

from .adminforms import PostAdminForm
from typeidea.base_admin import BaseOwnerAdmin
from .models import Post,Category,Tag
# from typeidea.custom_site import custom_site
# Register your models here.


class PostIniline(admin.TabularInline):
    form_layout=(
        Container(
            Row('title','desc'),
        )
    )

    extra = 1
    model = Post


@xadmin.sites.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    list_display = ('name','status','is_nav','created_time','owner','post_count')
    fields = ('name','status','is_nav')
    inlines = [PostIniline,]
    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(CategoryAdmin,self).save_model(request,obj,form,change)
    def post_count(self,obj):
        return obj.post_set.count()
    post_count.short_description = "文章数量"



class TagAdmin(BaseOwnerAdmin):
    list_display = ('name','status','created_time')
    fields = ('name','status')

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(TagAdmin,self).save_model(request,obj,form,change)
xadmin.site.register(Tag, TagAdmin)

class CategoryOwnerFilter(RelatedFieldListFilter):

    @classmethod
    def test(cls,field,request,params,model,admin_view,field_path):
        return field.name =='category'

    def __init__(self,field,request,params,model,model_admin,field_path):
        super().__init__(field,request,params,model,model_admin,field_path)
        self.lookup_choices = Category.objects.filter(owner=request.user).values_list('id','name')
manager.register(CategoryOwnerFilter,take_priority=True)



class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm

    list_display = [
        'title', 'category', 'status',
        'pv', 'uv', 'created_time', 'operator'
    ]
    list_display_links = []
    exclude = ('html', 'owner', 'pv', 'uv')

    list_filter = ['category', ]
    search_fields = ['title', 'category__name']
    save_on_top = True

    actions_on_top = True
    actions_on_bottom = True

    # 编辑页面
    save_on_top = True

    form_layout = (
        Fieldset(
           '基础信息',
            Row("title",'category'),
            'status',
            'tag',
        ),
        Fieldset(
            '内容信息',
            'desc',
            'is_md',
            'content_ck',
            'content_md',
            'content',
        )
    )

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )
    operator.short_description = '操作'

xadmin.site.register(Post, PostAdmin)



# class LogEntryAdmin(admin.ModelAdmin):
#     list_display = ['object_repr','object_id','action_flag','user',
#             'change_message']
# xadmin.site.register(LogEntry, LogEntryAdmin)
