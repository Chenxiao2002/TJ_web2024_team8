import uuid
from djongo import models

class Post(models.Model):
    """ 帖子表 """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    uid = models.UUIDField(verbose_name='用户ID')
    title = models.CharField(max_length=64, verbose_name='标题')
    content = models.TextField(max_length=3000, verbose_name='内容', null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'Post'  # 指定集合名称为 'Post'

    def __str__(self):
        return self.title
