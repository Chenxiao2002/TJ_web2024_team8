from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from blog.models import Post

# Create your models here.
"""评论表的模型"""
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    
    #评论的内容
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE) #这个字段是关联ContentType表的，ContentType是存储模型的表
    object_id = models.PositiveIntegerField() #这个是关联模型的主键
    content_object = GenericForeignKey('content_type', 'object_id')
    
    #对应text字段，评论的内容
    content = models.TextField(max_length=3000, verbose_name='评论', null=False)
    
    #对应评论的创建时间comment_time
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    #parent_comment是对应的父评论，如果是回复的话
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    
    root = models.ForeignKey('self', related_name='root_comment', null=True, on_delete=models.CASCADE)
    
    # parent = models.ForeignKey('self', related_name='parent_comment', null=True, on_delete=models.CASCADE)
    reply_to = models.ForeignKey(User, related_name="replies", null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.text

    class Meta:
        ordering = ['comment_time']
