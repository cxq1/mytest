from django import template

from comment.form import CommenForm
from comment.models import Comment

register = template.Library()

@register.inclusion_tag('comment/block.html')
def comment_block(target):
    return {
        'target':target,
        'comment_form':CommenForm(),
        'comment_list':Comment.get_by_target(target)
    }