from djongo import models
from bson import ObjectId

class Post(models.Model):
    """ 帖子表 """
    _id = models.ObjectIdField()
    uid = models.CharField(max_length=24, verbose_name='用户ID', null=False)
    title = models.CharField(max_length=64, verbose_name='标题')
    content = models.TextField(max_length=3000, verbose_name='内容', null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    class Meta:
        db_table = 'Post'  # 指定集合名称为 'Post'
