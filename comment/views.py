from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView

# Create your views here.
from comment.forms import CommentForm
from comment.models import Comment


class CommentView(TemplateView):
    http_method_names = ['post']
    template_name = 'comment/result.html'

    def post(self,request,*args,**kwargs):
        referer = request.META.get('HTTP_REFERER', reverse('index'))

        commentForm = CommentForm(request.POST)
        comment = Comment()
        if commentForm.is_valid():
            # commentForm.save()
            comment.content = commentForm.cleaned_data['content']
            comment.content_object=commentForm.cleaned_data['content_object']

            comment.nickname=commentForm.cleaned_data['nickname']
            comment.email=commentForm.cleaned_data['email']
            comment.user_id=1
            comment.save()

            succeed=True
            return redirect(referer)
        else:
            succeed=False

        context={
            'succeed':succeed,
            'form':comment,
            'target':referer,
        }
        return self.render_to_response(context)

