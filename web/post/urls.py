from django.urls import path
from . import views

urlpatterns=[
    path('upload_post/', views.upload_post, name='upload_post'),  # 用户上传帖子图片
    path('upload_post_info/', views.upload_post_info, name='upload_post_info'),  # 用户上传帖子信息
    path('get_post_detail/', views.get_post_detail, name='get_post_detail'),  # 获取帖子详情
    path('query_post_index/', views.query_post_index, name='query_post_index'),  # 主页推送帖子
    path('control_like_collect/', views.control_like_collect, name='control_like_collect'),  # 控制点赞和收藏
    path('post_delete/', views.post_delete, name='post_delete'),  # 删除帖子
]
