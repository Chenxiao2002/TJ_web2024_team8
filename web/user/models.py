# from django.db import models 

# class User(models.Model):
#     """ 用户表 """
#     email = models.CharField(max_length=32, verbose_name='邮箱', null=False, default='123@123.com')
#     username = models.CharField(max_length=32, verbose_name='用户名', null=False)
#     password = models.CharField(max_length=64, verbose_name='密码', null=False)
#     avatar = models.CharField(max_length=256, verbose_name='头像', null=False,
#                               default='http://localhost:8000/static/img/avatar/defaultAvatar.jpg')
#     signature = models.CharField(max_length=64, verbose_name='个性签名', default='暂时没有个性签名~', null=True)
#     # 用户关注，related_name获取用户的粉丝
#     following = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='beFocusOn')
#     # 用户喜爱的帖子
#     favorites = models.ManyToManyField('Post', blank=True, related_name='favoritePosts')
#     # 用户收藏的帖子
#     collected = models.ManyToManyField('Post', blank=True, related_name='collectedPosts')
#     #用户昵称
#     nickname = models.CharField(max_length=20)
#     #用户等级
#     level=models.IntegerField(default=0)

# class Post(models.Model):
#     """ 帖子表 """
#     # 用户通过related_name获取ta发的帖子
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
#     title = models.CharField(max_length=64, verbose_name='标题', null=False)
#     content = models.TextField(max_length=3000, verbose_name='内容', null=True)
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

#     def delete(self, *args, **kwargs):
#         # 删除关联的帖子图片
#         self.imgs.all().delete()
#         # 删除帖子的图片的存储
#         path = SYSTEM_PATH + 'post/'
#         check_and_delete(mainPath=path, id=self.id)
#         # 删除帖子本身
#         super().delete(*args, **kwargs)

from djongo import models
from bson import ObjectId

class Profile(models.Model):
    _id = models.ObjectIdField()  # 这里定义 _id 是为了明确这个模型是独立的文档
    pid = models.CharField(max_length=24)
    class Meta:
        abstract = True  # 这个模型不会创建单独的数据库表
class User(models.Model):
    """ 用户表 """
    _id = models.ObjectIdField()
    email = models.CharField(max_length=32, verbose_name='邮箱', null=False, default='123@123.com')
    username = models.CharField(max_length=32, verbose_name='用户名', null=False)
    password = models.CharField(max_length=64, verbose_name='密码', null=False)
    avatar = models.CharField(max_length=256, verbose_name='头像', null=False,
                              default='http://localhost:8000/static/img/avatar/defaultAvatar.jpg')
    signature = models.CharField(max_length=64, verbose_name='个性签名', default='暂时没有个性签名~', null=True)
    following = models.ArrayField(
        model_container=Profile,  # 使用字符型字段存储其他用户的 ID
        default=list,
        blank=True
    )
    favorites = models.ArrayField(
        model_container=Profile,  # 使用字符型字段存储帖子的 ID
        default=list,
        blank=True
    )
    collected = models.ArrayField(
        model_container=Profile,  # 使用字符型字段存储帖子的 ID
        default=list,
        blank=True
    )
    nickname = models.CharField(max_length=20)
    level = models.IntegerField(default=0)
    class Meta:
        db_table = 'User'  # 指定集合名称为 'User'

class Post(models.Model):
    """ 帖子表 """
    _id = models.ObjectIdField()
    uid = models.CharField(max_length=24, verbose_name='用户ID', null=False)
    title = models.CharField(max_length=64, verbose_name='标题')
    content = models.TextField(max_length=3000, verbose_name='内容', null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    class Meta:
        db_table = 'Post'  # 指定集合名称为 'Post'