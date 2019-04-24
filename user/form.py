from django import forms
from django.contrib import auth

from .models import UserInfo

class LoginForm(forms.Form):
    username=forms.CharField(
        label='用户名',
        max_length=50,
        widget=forms.widgets.Input()
    )

    password = forms.CharField(
        label='密码',
        max_length=50,
        widget=forms.widgets.PasswordInput()
    )

    def clean(self):
        username=self.cleaned_data['username']
        password = self.cleaned_data['password']

        user = auth.authenticate(username=username,password=password)
        if user is None:
            raise forms.ValidationError("用户名或密码不正确")
        else:
            self.cleaned_data['user'] =user
        return self.cleaned_data

    class Meta:
        model =UserInfo
        fields=['username','password']


class Regfrom(forms.Form):
    username=forms.CharField(
        label='用户名',
        max_length=10,
        widget=forms.widgets.Input()
    )
    email =forms.EmailField(
        label='邮箱',
        max_length=20,
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': '请输入邮箱'}
        )
    )
    password1 = forms.CharField(
        label='密码',
        max_length=20,
        widget=forms.widgets.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '再输入一次密码'}
        )
    )

    password2 = forms.CharField(
        label='密码',
        max_length=20,
        widget=forms.widgets.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '再输入一次密码'}
        )
    )

    def clean_username(self):
        username= self.cleaned_data['username']
        if UserInfo.objects.filter(username=username).exists():
            raise forms.ValidationError("用户名已经存在")
        return username
    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1!=password2:
            raise forms.ValidationError("密码不一致")
        return password2
    def clean_email(self):
        email = self.cleaned_data['email']
        if UserInfo.objects.filter(email=email).exists():
            raise  forms.ValidationError("邮箱已经存在")

