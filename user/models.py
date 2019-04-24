from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class UserInfo(AbstractUser):
    nickname=models.CharField(max_length=20,verbose_name='昵称',blank=True,null=True)
    qq =models.CharField(max_length=20,verbose_name='qq号码',blank=True)
    phone = models.CharField(max_length=11,verbose_name='手机号码',blank=True)

    class Meta:
        verbose_name_plural =verbose_name='用户'
        ordering=['-id']

    def __str__(self):
        return self.username

