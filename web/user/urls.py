from django.urls import path
from . import views


urlpatterns = [
    #path('login_for_medal/', views.login_for_medal, name='login_for_medal'),
    #path('login/', views.login, name='login'),
    #path('register/', views.register, name='register'),
    # path('logout/', views.logout, name='logout'),
    # path('user_info/', views.user_info, name='user_info'),
    # path('change_nickname/', views.change_nickname, name='change_nickname'),
    # path('bind_email/', views.bind_email, name='bind_email'),
    # path('send_verification_code/', views.send_verification_code, name='send_verification_code'),
    # path('change_password/', views.change_password, name='change_password'),
    # path('forgot_password/', views.forgot_password, name='forgot_password'),
    #add
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