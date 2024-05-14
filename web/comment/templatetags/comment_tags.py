from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Comment
from ..forms import CommentForm


register = template.Library()

"""这段代码在论坛的后端用于处理与评论相关的操作，包括获取评论数量、获取评论表单和获取评论列表。"""
@register.simple_tag
def get_comment_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(content_type=content_type, object_id=obj.pk).count()

@register.simple_tag
def get_comment_form(obj):
    content_type = ContentType.objects.get_for_model(obj)
    form = CommentForm(initial={
            'content_type': content_type.model, 
            'object_id': obj.pk, 
            'reply_comment_id': 0})
    return form

@register.simple_tag
def get_comment_list(obj):
    content_type = ContentType.objects.get_for_model(obj)
    comments = Comment.objects.filter(content_type=content_type, object_id=obj.pk, parent=None)
    return comments.order_by('-comment_time')
    