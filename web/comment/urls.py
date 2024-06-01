from django.urls import path
from . import views


urlpatterns = [
    path('comment/', comment.do_comment),
    path('comment/main/', comment.get_comment),
    path('comment/reply/', comment.load_reply)
]