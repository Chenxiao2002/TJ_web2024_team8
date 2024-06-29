from django.shortcuts import render
import string
import random
import time
import json
from post.models import Post
from user.models import User,Image,Favorites,Collects,Follows
from comment.models import Comment
from bson import ObjectId
from user.utils import authenticate_request
from post.utils import convert_to_timezone
from django.http import JsonResponse
from web.settings import TIME_ZONE,BASE_DIR
from django.db.models import Q
# Create your views here.

@authenticate_request
def get_info_comment(request,payload):
    user_id = payload['user_id']
    posts=Post.objects.filter(uid=user_id)
    post_ids=[str(post._id) for post in posts]
    comments = Comment.objects.filter(Q(pid__in=post_ids)).order_by('-created_at')
    if comments:
        data=[]
        for comment in comments:
            if comment:
                user=User.objects.filter(_id=ObjectId(comment.uid)).first()
                img=Image.objects.filter(pid=comment.pid).first()
                if img:
                    img_path=img.imagePath
                else:
                    img_path=str(BASE_DIR)+"/media/img/default.jpg"
                comment_parent=""
                comment_child=""
                if comment.parent_cid=="#":
                    comment_parent=comment.content
                else:
                    comment_parent=Comment.objects.filter(_id=ObjectId(comment.parent_cid)).first().content
                    comment_child=comment.content
                comment_data={
                    'username': user.username,  #评论者名称
                    'avatar': user.avatar,      #评论者头像
                    'createTime': convert_to_timezone(comment.created_at, TIME_ZONE), #评论时间
                    'post_img0':img_path,       #帖子图片
                    'comment_p':comment_parent, #一级评论内容
                    'comment_c':comment_child,  #二级评论内容，如果此评论为一级评论，则此项为空
                    'post_id': comment.pid
                }
                data.append(comment_data)
        return JsonResponse({'info': data}, status=200)
    return JsonResponse({'info': []}, status=200)

@authenticate_request
def get_info_like(request,payload):
    user_id = payload['user_id']
    posts=Post.objects.filter(uid=user_id)
    post_ids=[str(post._id) for post in posts]
    likes = Favorites.objects.filter(Q(pid__in=post_ids)).order_by('-favorite_time')
    if likes:
        data=[]
        for like in likes:
            if like:
                user=User.objects.filter(_id=ObjectId(like.uid)).first()
                img=Image.objects.filter(pid=like.pid).first()
                if img:
                    img_path=img.imagePath
                else:
                    img_path=str(BASE_DIR)+"/media/img/default.jpg"
                like_data={
                    'username': user.username,
                    'avatar': user.avatar,
                    'createTime': convert_to_timezone(like.favorite_time, TIME_ZONE),
                    'post_img0':img_path,
                    'post_id':like.pid
                }
                data.append(like_data)
        return JsonResponse({'info': data}, status=200)
    return JsonResponse({'info': []}, status=200)

@authenticate_request
def get_info_collect(request,payload):
    user_id = payload['user_id']
    posts=Post.objects.filter(uid=user_id)
    post_ids=[str(post._id) for post in posts]#用户发布的帖子id
    collects = Collects.objects.filter(Q(pid__in=post_ids)).order_by('-collect_time')
    if collects:
        data=[]
        for collect in collects:
            if collect:
                user=User.objects.filter(_id=ObjectId(collect.uid)).first()
                img=Image.objects.filter(pid=collect.pid).first()
                if img:
                    img_path=img.imagePath
                else:
                    img_path=str(BASE_DIR)+"/media/img/default.jpg"
                collect_data={
                    'username': user.username,
                    'avatar': user.avatar,
                    'createTime': convert_to_timezone(collect.collect_time, TIME_ZONE),
                    'post_img0':img_path,
                    'post_id':collect.pid
                }
                data.append(collect_data)
        return JsonResponse({'info': data}, status=200)
    return JsonResponse({'info': []}, status=200)

@authenticate_request
def get_info_focus(request, payload):
    user_id = payload['user_id']
    follows = Follows.objects.filter(lid=user_id).order_by('-follow_time')
    if follows:
        data=[]
        for follow in follows:
            if follow:
                f_user=User.objects.filter(_id=ObjectId(follow.fid)).first()
                back_follow=Follows.objects.filter(fid=user_id,lid=follow.fid).first()
                if back_follow:
                    is_back_follow=True
                else:
                    is_back_follow=False

                collect_data={
                    'id': str(f_user._id),
                    'username': f_user.username,
                    'avatar': f_user.avatar,
                    'createTime': convert_to_timezone(follow.follow_time, TIME_ZONE),
                    'back':is_back_follow    #bool类型
                }
                data.append(collect_data)
        return JsonResponse({'info': data}, status=200)
    return JsonResponse({'info': []}, status=200)

@authenticate_request
def get_info_follows(request, payload):
    user_id = payload['user_id']
    follows = Follows.objects.filter(fid=user_id).order_by('-follow_time')
    if follows:
        data=[]
        for follow in follows:
            if follow:
                l_user=User.objects.filter(_id=ObjectId(follow.lid)).first()
                back_follow=Follows.objects.filter(fid=follow.lid,lid=user_id).first()
                if back_follow:
                    is_back_follow=True
                else:
                    is_back_follow=False

                collect_data={
                    'id': str(l_user._id),
                    'username': l_user.username,
                    'avatar': l_user.avatar,
                    'createTime': convert_to_timezone(follow.follow_time, TIME_ZONE),
                    'back':is_back_follow    #bool类型
                }
                data.append(collect_data)
        return JsonResponse({'info': data}, status=200)
    return JsonResponse({'info': []}, status=200)


    



