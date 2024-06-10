from django.urls import path
from . import views
from comment import views as comment

urlpatterns = [
    path('post/', views.query_post_index, name='query_post_index'),
    path('post/detail/', views.get_post_detail, name='get_post_detail'),
    path('post/delete/', views.post_delete, name='post_delete'),
    path('post/control/', views.control_like_collect, name='control_like_collect'),
    path('upload/info/', views.upload_post_info, name='upload_post_info'),
    path('upload/', views.upload_post, name='upload_post'),
]
