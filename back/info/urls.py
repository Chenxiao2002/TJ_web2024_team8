from django.urls import path
from . import views


urlpatterns = [
    path("getCollectInfo/", views.get_info_collect, name='get_info_collect'),
    path("getCommentInfo/", views.get_info_comment, name='get_info_comment'),
    path("getLikeInfo/", views.get_info_like, name='get_info_like'),
    path("getFocusInfo/", views.get_info_focus, name='get_info_focus'),
    path("getFollowsInfo/", views.get_info_follows, name='get_info_follows'),
]