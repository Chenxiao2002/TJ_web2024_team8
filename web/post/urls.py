from django.urls import path
from . import views
from comment import views as comment

urlpatterns = [
    path('comment/', comment.do_comment, name='do_comment'),
    path('comment/main/', comment.get_comment, name='get_comment'),
    path('comment/reply/', comment.load_reply, name='load_reply'),
    path('post/', views.query_post_index, name='query_post_index'),
    path('post/detail/', views.get_post_detail, name='get_post_detail'),
    path('post/delete/', views.post_delete, name='post_delete'),
    path('post/like_collect/', views.control_like_collect, name='control_like_collect'),
    path('post/upload_info/', views.upload_post_info, name='upload_post_info'),
    path('post/upload/', views.upload_post, name='upload_post'),
]
