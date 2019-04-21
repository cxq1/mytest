from datetime import date

from django.core.cache import cache
from django.db.models import Q, F
from django.views.generic import ListView,DetailView
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from comment.models import Comment
from .models import Category,Post,Tag
from config.models import *
from comment.form import CommenForm

class CommonViewMixin:
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars':SideBar.get_all(),
        })
        context.update(Category.get_nvas())
        return context

class IndexView(CommonViewMixin,ListView):
    queryset = Post.latest_post()
    paginate_by = 1
    context_object_name = 'post_list'
    template_name = 'blog/list.html'

class AuthorView(IndexView):
    def get_queryset(self):
        queryset = super().get_queryset()
        author_id = self.kwargs.get('owner_id')
        return queryset.filter(owner_id=author_id)

class SearchView(IndexView):
    def get_context_data(self):
        context = super().get_context_data()
        context.update({
            'keyword':self.request.GET.get('keyword','')
        })
        return context
    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return queryset
        return queryset.filter(Q(title__icontains=keyword)|Q(desc__icontains=keyword))



class CategoryView(IndexView):
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category,pk=category_id)
        context.update({
            'category':category,

        })
        return context
    def get_queryset(self):
        queryset = super().get_queryset()
        category_id=self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)

class TagView(IndexView):
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag,pk=tag_id)
        context.update({
            'tag':tag,
        })
        return context
    def get_queryset(self):
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag__id=tag_id)

class PostDetailView(CommonViewMixin,DetailView):
    queryset = Post.latest_post()
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    # def get_context_data(self,**kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context.update({
    #         'comment_form':CommenForm,
    #         'comment_list':Comment.get_by_target(self.request.path),
    #
    #     })
    #     return context

    def get(self, request, *args, **kwargs):
        response = super().get(request,*args,**kwargs)
        self.handle_visited()
        return response

    def handle_visited(self):
        increase_pv = False
        increase_uv = False
        uid = self.request.uid
        pv_key = 'pv:%s:%s'%(uid,self.request.path)
        uv_key = 'uv:%s:%s:%s'%(uid,str(date.today()),self.request.path)

        if not cache.get(pv_key):
            increase_pv= True
            cache.set(pv_key,1,1*60)
        if not cache.get(uv_key):
            increase_uv=True
            cache.set(uv_key,1,24*60*60)
        if increase_uv and increase_pv:
            Post.objects.filter(pk =self.object.id).update(pv=F('pv')+1,uv=F('uv')+1)
        elif increase_pv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1)
        elif increase_uv:
            Post.objects.filter(pk=self.object.id).update(uv=F('uv') + 1)

def post_list(request, category_id=None, tag_id=None):
    tag=None
    category=None
    if tag_id:
        tag,post_list = Post.get_by_tag(tag_id)
    elif category_id:
        category,post_list = Post.get_by_category(category_id)
    else:
        post_list = Post.latest_post()

    context={
        'tag':tag,
        'category':category,
        'post_list':post_list,
        'sidebars':SideBar.get_all(),
    }
    context.update(Category.get_nvas())

    return render(request,'blog/list.html',context=context)

def post_detail(requst,post_id=None):
    try:
        post =Post.objects.get(id=post_id)
    except Post.DoesNotExit:
        post = None
    context={
        'post':post,
        'sidebars': SideBar.get_all(),
    }
    context.update(Category.get_nvas())
    return render(requst,'blog/detail.html',context=context)
