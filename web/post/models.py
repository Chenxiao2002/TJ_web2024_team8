import os
from django.db import models
from django.contrib.auth.models import User
from web.settings import SYSTEM_PATH

# Create your models here.
class Post(models.Model):
    """ 帖子表 """
    # 用户通过related_name获取ta发的帖子
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=64, verbose_name='标题', null=False)
    content = models.TextField(max_length=3000, verbose_name='内容', null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def delete(self, *args, **kwargs):
        # 删除关联的帖子图片
        self.imgs.all().delete()
        # 删除帖子的图片的存储
        path = SYSTEM_PATH + 'post/'
        check_and_delete(mainPath=path, id=self.id)
        # 删除帖子本身
        super().delete(*args, **kwargs)   

# 检查和删除图片，用于删除帖子时删除文件，以及删除用户上一次上传的头像
def check_and_delete(*, id, mainPath):
    # 获取目录下的文件
    file_list = os.listdir(mainPath)
    # 遍历文件列表，检查是否有对应的文件，如果有就删除
    for file_name in file_list:
        if file_name.startswith(f'{id}-'):
            file_path = os.path.join(mainPath, file_name)
            os.remove(file_path)

