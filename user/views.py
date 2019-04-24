from django.contrib.auth import authenticate
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import auth
from django.urls import reverse
from django.views.generic import TemplateView
from .form import LoginForm,Regfrom
from .models import UserInfo
# Create your views here.

class login(TemplateView):

    http_method_names = ['post','get']

    def post(self,request,*args,**kwargs):
        loginForm = LoginForm(request.POST)
        succeed = None

        if loginForm.is_valid():
            username= loginForm.cleaned_data['username']
            password = loginForm.cleaned_data['password']
            print(password)
            user = authenticate(username=username,password=password)
            auth.login(request,user)
            succeed = True
            request.session['succeed']=succeed
            return redirect(request.GET.get('from',reverse('index')))
        else:
            print("err")
            succeed=False
            return  redirect(reverse('index'))
        context = {
            'succeed':succeed,
            'loginform':loginForm,
        }
        return render(request,'blog/list.html',context)

    def get(self, request, *args, **kwargs):

        loginform= LoginForm()
        return render(request,'user/login.html',locals())

class registerView(TemplateView):
    def post(self,request):
        regForm= Regfrom(request.POST)
        succeed=None
        if regForm.is_valid():
            username=regForm.cleaned_data['username']
            password =regForm.cleaned_data['password2']
            email = regForm.cleaned_data['email']
            user = UserInfo.objects.create_user(username=username,password=password,email=email)
            user.save()
            user= auth.authenticate(username=username,password=password)
            auth.login(request,user)
            return redirect(request.GET.get('from',reverse('index')))


    def get(self, request, *args, **kwargs):
        registerform = Regfrom()
        return render(request,'user/register.html',locals())

