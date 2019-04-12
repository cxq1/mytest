"""typeidea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from .custom_site import custom_site

from blog.views import post_list,post_detail


urlpatterns = [
    url(r'^$',post_list,name='index'),
    url(r'^category/(?P<category_id>\d+)/$',post_list,name='category-list'),
    url(r'^tag/(?P<tag_id>\d+)/$',post_list,name='tag-list'),
    url(r'^post/(?P<post_id>\d+).html/$',post_detail,name='post-detail'),
    url(r'^super_admin/',admin.site.urls),
    url(r'^admin/', custom_site.urls),
]
