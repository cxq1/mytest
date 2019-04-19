from django import template

from comment.forms import CommetnForm
from comment.models import Comment

register = template.Library()

@register.inclusion_tag('comment/block.html')

def comment_block(target):
    return {
        'target':target,
        'comment_form':CommetnForm(),
        'comment_list':Comment.get_by_target(target),
    }