from django.shortcuts import render
from .models import Category,Post,Tag
from config.models import *

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
