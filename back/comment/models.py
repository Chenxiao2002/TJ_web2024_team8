from djongo import models
from bson import ObjectId

class Comment(models.Model):
    """ 评论表 """
    _id = models.ObjectIdField()
    pid = models.CharField(max_length=24, verbose_name='帖子ID', null=False)
    uid = models.CharField(max_length=24, verbose_name='用户ID', null=False)
    content = models.TextField(max_length=3000, verbose_name='评论', null=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    parent_cid = models.CharField(max_length=24, verbose_name='上级评论ID', null=False)
    class Meta:
        db_table = 'Comment'