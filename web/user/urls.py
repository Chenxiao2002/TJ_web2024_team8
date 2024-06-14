from django.urls import path
from . import views


urlpatterns = [
    path("login/", views.login, name='login'),
    path('register/', views.register,name='register'),
    path('user/focus/', views.get_user_focus),
    path('user/avatar/', views.update_avatar),
    path('user/update/', views.update_user_info),
    path('focus/', views.focusOn),
    path('user/unfollow/', views.unfollow),
    path('user/remove/fan/', views.remove_fans),
    path('index/', views.query_user_index,name='user_info'),
    path('user/post/', views.query_user_index_post),
    path('user/post/control/', views.user_control_index),
]