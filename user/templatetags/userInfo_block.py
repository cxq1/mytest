from django import template

from user.form import LoginForm

register = template.Library()

@register.inclusion_tag('user/login.html')
def login_block():
    return {
        'loginform':LoginForm
    }