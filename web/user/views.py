import string
import random
import time
import json
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import JsonResponse
from django.core.mail import send_mail
from .models import *
from post.models import Post
from django.core.paginator import Paginator
from .utils import *
from web.settings import SYSTEM_PATH
from bson import ObjectId

# 用户登录
def login(request):
    data = json.loads(request.body)
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return JsonResponse({'error': '缺少必要的邮箱或密码'}, status=400)
    user = User.objects.filter(email=email, password=password).first()
    error_message = {'error': '邮箱或密码错误'}
    if user :
        token = create_token(user)
        user = {
            'id': str(user._id),
            'username': user.username,
            'avatar': user.avatar,
            'signature': user.signature,
            'token': token
        }
        return JsonResponse(user, status=200)
    return JsonResponse(error_message, status=401)

# 用户注册
def register(request):
    data = json.loads(request.body)
    email = data.get('email')
    username=data.get('username')
    password=data.get('password')
    if check_email(email):
        return JsonResponse({'error': '该邮箱已被注册'}, status=401)
    try:
        User.objects.create(email=email,username=username,password=password)
        return JsonResponse({'info': '创建用户成功'})
    except Exception as e:
        print(e)
        return JsonResponse({'error': '创建用户失败'}, status=401)

# 获取用户关注，收藏帖子以及喜欢帖子
@authenticate_request
def get_user_focus(request,payload):
    #data = json.loads(request.body)
    #user_id = data.get('user_id')
    user_id = payload['user_id']
    follows = Follows.objects.filter(fid=user_id)
    fo_ids = [u.lid for u in follows]
    collects = Collects.objects.filter(uid=user_id)
    co_ids = [u.pid for u in collects]
    favorites = Favorites.objects.filter(uid=user_id)
    fa_ids = [u.pid for u in favorites]
    return JsonResponse({'info': {
        'follow': fo_ids, 'collected': co_ids, 'favorites': fa_ids
    }}, status=200)

# 上传头像
@authenticate_request
def update_avatar(request, payload):
    file = request.FILES['file']
    id = payload['user_id']
    file_path = SYSTEM_PATH + 'avatar/' + id + '-' + file.name
    check_and_delete(id=id, mainPath=SYSTEM_PATH + 'avatar/')
    with open(file_path, 'wb') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    result = {
        'filename': file.name,
        'filepath': 'http://localhost:8000/static/img/avatar/' + id + '-' + file.name,
    }
    user = User.objects.filter(id=id).first()
    user.avatar = 'http://localhost:8000/static/img/avatar/' + id + '-' + file.name
    user.save()
    return JsonResponse({'info': result}, status=200)

# 修改用户信息
#@authenticate_request
def update_user_info(request,payload):
    data = json.loads(request.body)
    user_id = payload['user_id']
    user = User.objects.filter(_id=ObjectId(user_id)).first()
    user.username = data['username']
    user.signature = data['signature']
    user.save()
    return JsonResponse({'info': '修改成功'}, status=200)

# 用户关注
@authenticate_request
def focusOn(request):
    # 做关注操作的用户id
    id1 = payload['user_id']
    user1 = User.objects.filter(_id=ObjectId(id1)).first()
    # 被关注的用户id
    id2 = json.loads(request.body)['id']
    user2 = User.objects.filter(_id=ObjectId(id2)).first()
    if user1 and user2:
        Follows.objects.create(fid=id1,lid=id2)
        return JsonResponse({'info': '成功关注'}, status=200)
    return JsonResponse({'error': '非法的操作'}, status=401)

#取消关注
@authenticate_request
def unfollow(request, payload):
    # 取消关注操作的用户id
    user_id = payload['user_id']
    # 被取消关注的用户id
    unfollow_id = json.loads(request.body)['id']
    unfollow_info = Follows.objects.filter(fid=user_id,lid=unfollow_id).first()
    if unfollow_info:
        unfollow_info.delete()
        return JsonResponse({'info': '成功取消关注'}, status=200)
    return JsonResponse({'error': '非法的操作'}, status=401)

#移除粉丝
@authenticate_request
def remove_fans(request, payload):
    # 移除操作的用户id
    user_id = payload['user_id']
    # 移除的粉丝id
    fans_id = json.loads(request.body)['id']
    unfollow_info = Follows.objects.filter(fid=fans_id,lid=user_id).first()
    if user and fan:
        unfollow_info.delete()
        return JsonResponse({'info': '成功移除粉丝'}, status=200)
    return JsonResponse({'error': '非法的操作'}, status=401)

# 获取用户主页的个人信息
def query_user_index(request):
    data = json.loads(request.body)
    user_id=data.get('id')
    if user_id and user_id != 'undefined':
        user = User.objects.filter(_id=ObjectId(user_id)).first()
        fans_count=Follows.objects.filter(lid=user_id).count()
        focus_count=Follows.objects.filter(fid=user_id).count()
        posts_count=Post.objects.filter(uid=user_id).count()
        if user:
            author = {
                'id': str(user._id),
                'username': user.username,
                'avatar': user.avatar,
                'signature': user.signature,
                'fans': fans_count,
                'focusOn': focus_count,
                'postsCount': posts_count,
            }
            info = {
                'user': author,
            }
            return JsonResponse({'data': info}, status=200)
        return JsonResponse({'error': '错误的访问'}, status=404)
    return JsonResponse({'error': '非法访问'}, status=404)

#用户主页帖子
def query_user_index_post(request):
    type_mapping = {
        '帖子': 'posts',
        '点赞': 'favorites',
        '收藏': 'collected',
    }
    data = json.loads(request.body)
    user_id = data['user_id']
    types = data['types']
    offset = data['offset']
    user = User.objects.filter(_id=ObjectId(user_id)).first()
    if user and types in type_mapping:
        field_name = type_mapping[types]
        postObj=[]
        if field_name=='posts':
            postObj=Post.objects.filter(uid=user_id)
        elif field_name=='favorites':
            favorite_records = Favorites.objects.filter(uid=user_id)
            for favorite_record in favorite_records:
                pid = favorite_record.pid
                post = Post.objects.filter(_id=ObjectId(pid)).first()
                if post:
                    postObj.append(post)
        else:
            collect_records = Collects.objects.filter(uid=user_id)
            for collect_record in collect_records:
                pid = collect_record.pid
                post = Post.objects.filter(_id=ObjectId(pid)).first()
                if post:
                    postObj.append(post)
        posts = filter_querySet(postObj, offset, limit=10)
        if posts:
            return JsonResponse({'info': list(combine_index_post(posts))}, status=200)
        return JsonResponse({'info': []}, status=200)
    return JsonResponse({'error': '错误访问'}, status=404)

#用户管理页面数据获取
@authenticate_request
def user_control_index(request, payload):
    user_id = payload['user_id']
    data = json.loads(request.body)
    offset = data['offset']
    types = data['types']
    user = User.objects.filter(_id=ObjectId(user_id)).first()
    if user:
        if types == 'posts':
            user_data = Post.objects.filter(uid=user_id)
            info = get_user_post_info(user_data, offset)
        elif types == 'collected':
            collect_records = Collects.objects.filter(uid=user_id)
            user_data=[]
            for collect_record in collect_records:
                pid = collect_record.pid
                post = Post.objects.filter(_id=ObjectId(pid)).first()
                if post:
                    user_data.append(post)
            info = get_user_post_info(user_data, offset)
        elif types == 'favorites':
            favorite_records = Favorites.objects.filter(uid=user_id)
            user_data=[]
            for favorite_record in favorite_records:
                pid = favorite_record.pid
                post = Post.objects.filter(_id=ObjectId(pid)).first()
                if post:
                    user_data.append(post)
            info = get_user_post_info(user_data, offset)
        elif types == 'fans':
            fan_records=Follows.objects.filter(lid=user_id)
            user_data = []
            for fan_record in fan_records:
                uid=fan_record.fid
                fan=User.objects.filter(_id=ObjectId(uid)).first()
                if fan:
                    user_data.append(fan)
            info = get_user_info(user_data, offset)
        elif types == 'follow':
            follow_records=Follows.objects.filter(fid=user_id)
            user_data = []
            for follow_record in follow_records:
                uid=follow_record.lid
                follow=User.objects.filter(_id=ObjectId(uid)).first()
                if follow:
                    user_data.append(follow)
            info = get_user_info(user_data, offset)
        else:
            return JsonResponse({'error': '错误的操作'}, status=404)
        total = user_data.count()
        return JsonResponse({'info': info, 'total': total}, status=200)
    return JsonResponse({'error': '错误的操作'}, status=404)

