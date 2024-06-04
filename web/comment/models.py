import uuid
from django.db import models

class Comment(models.Model):
    """ 评论表 """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pid = models.UUIDField(verbose_name='帖子ID')
    uid = models.UUIDField(verbose_name='用户ID')
    content = models.TextField(max_length=3000, verbose_name='评论')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    parent_cid = models.UUIDField(verbose_name='上级评论ID', null=True, blank=True)

    class Meta:
        db_table = 'Comment'

    def __str__(self):
        return f"Comment by {self.uid} on {self.pid}"
