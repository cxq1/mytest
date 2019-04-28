from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from django.contrib.auth.models import User
from comment.models import Comment


class CommentForm(forms.ModelForm):
    nickname=forms.CharField(
        max_length=50,
        label='昵称',
        widget=forms.widgets.Input()
    )
    email = forms.CharField(
        label='email',
        max_length=20,
        widget=forms.widgets.EmailInput()
    )
    content= forms.CharField(
        label='内容',
        max_length='500',
        widget=forms.widgets.Textarea(
            attrs={'cows':6,'cols':60}
        )
    )
    content_type=forms.CharField(
        label='对象',
        widget=forms.widgets.HiddenInput()
    )
    object_id = forms.IntegerField(
        label='id对象',
        widget=forms.widgets.HiddenInput()
    )

    def clean_content(self):
        content = self.cleaned_data['content']
        if len(content)<1:
            raise forms.ValidationError("内容太短")
        return content
    def clean(self):
        content_type=self.cleaned_data.get('content_type')
        object_id =self.cleaned_data['object_id']

        try:
            model_class = ContentType.objects.get(model=content_type).model_class()

            model_obj = model_class.objects.get(pk=object_id)
            self.cleaned_data['content_object'] = model_obj
        except ObjectDoesNotExist:
            raise forms.ValidationError('评论对象不存在')

        return self.cleaned_data
    class Meta:
        model=Comment
        fields=['nickname','email','content']









    # content_type=forms.CharField(
    #     widget=forms.HiddenInput()
    # )
    # object_id = forms.CharField(
    #     widget=forms.widgets.HiddenInput()
    # )
    # content = forms.CharField(
    #     label='内容',
    #     max_length=100,
    #     widget=forms.widgets.Textarea(
    #         attrs={'cols':30,'rows':6}
    #     )
    # )
    #
    # def __init__(self,*args,**kwargs):
    #     if 'user' in kwargs:
    #         self.user = kwargs.pop("user")
    #     super(CommentForm, self).__init__(*args,**kwargs)
    #
    # def clean(self):
    #     # contenttype=self.cleaned_data['content_type']
    #     object_id = self.cleaned_data['object_id']
    #
    #     try:
    #         model_class = ContentType.objects.get(model=self.content_type).model_class()
    #         model_id = model_class.objects.get(pk=object_id)
    #         self.cleaned_data['contenttype'] =model_class
    #     except ObjectDoesNotExist:
    #         raise forms.ValidationError("评论对象不存在")
    #
    #     return self.cleaned_data
    #
    # class Meta:
    #     model = Comment
    #     fields=['content_type','content']