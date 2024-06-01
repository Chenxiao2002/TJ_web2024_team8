from djongo import models
from bson import ObjectId

class User(models.Model):
    """ 用户表 """
    _id = models.ObjectIdField()
    email = models.CharField(max_length=32, verbose_name='邮箱', null=False, default='123@123.com')
    username = models.CharField(max_length=32, verbose_name='用户名', null=False)
    password = models.CharField(max_length=64, verbose_name='密码', null=False)
    avatar = models.CharField(max_length=256, verbose_name='头像', null=False,
                              default='http://localhost:8000/static/img/avatar/defaultAvatar.jpg')
    signature = models.CharField(max_length=64, verbose_name='个性签名', default='暂时没有个性签名~', null=True)
    
    nickname = models.CharField(max_length=20)
    level = models.IntegerField(default=0)
    class Meta:
        db_table = 'User'  # 指定集合名称为 'User'

class Follows(models.Model):
    _id = models.ObjectIdField()
    fid = models.CharField(max_length=24)
    lid = models.CharField(max_length=24)
    follow_time= models.DateTimeField(auto_now_add=True, verbose_name='关注时间')
    class Meta:
        db_table = 'Follows'

class Favorites(models.Model):
    _id = models.ObjectIdField()
    uid = models.CharField(max_length=24)
    pid = models.CharField(max_length=24)
    favorite_time= models.DateTimeField(auto_now_add=True, verbose_name='点赞时间')
    class Meta:
        db_table = 'Favorites'

class Collects(models.Model):
    _id = models.ObjectIdField()
    uid = models.CharField(max_length=24)
    pid = models.CharField(max_length=24)
    collect_time= models.DateTimeField(auto_now_add=True, verbose_name='收藏时间')
    class Meta:
        db_table = 'Collects'

class Image(models.Model):
    _id = models.ObjectIdField()
    pid = models.CharField(max_length=24, verbose_name='帖子ID', null=False)
    imagePath = models.CharField(max_length=256, verbose_name='帖子图片')
    height = models.IntegerField(default=0, verbose_name='图片高度')
    width = models.IntegerField(default=0, verbose_name='图片宽度')
    class Meta:
        db_table = 'Image'
