from django.urls import path
from . import views

urlpatterns =[
    path('post/', post.query_post_index),
    path('post/detail/', post.get_post_detail),
    path('post/delete/', post.post_delete),
    path('post/control/', post.control_like_collect),
    path('upload/info/', post.upload_post_info),
    path('upload/', post.upload_post),
]
