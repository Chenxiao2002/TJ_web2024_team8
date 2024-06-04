import json
import string
import random
import time
from PIL import Image as PIL_Image
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import JsonResponse
from django.core.mail import send_mail
from .models import *
from post.models import Post
from comment.models import Comment
from django.core.paginator import Paginator
from .utils import *
from web.settings import SYSTEM_PATH, TIME_ZONE
from bson import ObjectId
from django.views.decorators.http import require_http_methods

# 用户登录
@require_http_methods(["POST"])
def login(request):
    try:
        print("receive login request",request.body)
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return JsonResponse({'error': '缺少必要的邮箱或密码'}, status=400)
        user = User.objects.filter(email=email, password=password).first()
        if user:
            token = create_token(user)#生成token
            user_data = {
                'id': str(user._id),
                'username': user.username,
                'avatar': user.avatar,
                'signature': user.signature,
                'token': token
            }
            return JsonResponse(user_data, status=200)
        return JsonResponse({'error': '邮箱或密码错误'}, status=401)
    except Exception as e:
        print("login error",str(e))
        return JsonResponse({'error': str(e)}, status=400)#这个情况是服务器错误

# 用户注册
def register(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        if check_email(email):
            return JsonResponse({'error': '该邮箱已被注册'}, status=401)
        User.objects.create(email=email, username=username, password=password)
        return JsonResponse({'info': '创建用户成功'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# 获取用户关注，收藏帖子以及喜欢帖子
@authenticate_request
def get_user_focus(request, payload):
    try:
        user_id = payload['user_id']
        follows = Follows.objects.filter(fid=user_id)
        fo_ids = [str(u.lid) for u in follows]
        collects = Collects.objects.filter(uid=user_id)
        co_ids = [str(u.pid) for u in collects]
        favorites = Favorites.objects.filter(uid=user_id)
        fa_ids = [str(u.pid) for u in favorites]
        return JsonResponse({'info': {
            'follow': fo_ids, 'collected': co_ids, 'favorites': fa_ids
        }}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# 上传头像
@authenticate_request
def update_avatar(request, payload):
    try:
        file = request.FILES['file']
        user_id = payload['user_id']
        file_path = SYSTEM_PATH + 'avatar/' + user_id + '-' + file.name
        check_and_delete(id=user_id, mainPath=SYSTEM_PATH + 'avatar/')
        with open(file_path, 'wb') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        result = {
            'filename': file.name,
            'filepath': 'http://localhost:8000/static/img/avatar/' + user_id + '-' + file.name,
        }
        user = User.objects.filter(id=ObjectId(user_id)).first()
        user.avatar = result['filepath']
        user.save()
        return JsonResponse({'info': result}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# 修改用户信息
@authenticate_request
def update_user_info(request, payload):
    try:
        data = json.loads(request.body)
        user_id = payload['user_id']
        user = User.objects.filter(id=ObjectId(user_id)).first()
        user.username = data['username']
        user.signature = data['signature']
        user.save()
        return JsonResponse({'info': '修改成功'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# 用户关注
@authenticate_request
def focusOn(request, payload):
    try:
        user_id = payload['user_id']
        follow_id = json.loads(request.body)['id']
        user1 = User.objects.filter(id=ObjectId(user_id)).first()
        user2 = User.objects.filter(id=ObjectId(follow_id)).first()
        if user1 and user2:
            Follows.objects.create(fid=user_id, lid=follow_id)
            return JsonResponse({'info': '成功关注'}, status=200)
        return JsonResponse({'error': '非法的操作'}, status=401)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# 取消关注
@authenticate_request
def unfollow(request, payload):
    try:
        user_id = payload['user_id']
        unfollow_id = json.loads(request.body)['id']
        unfollow_info = Follows.objects.filter(fid=user_id, lid=unfollow_id).first()
        if unfollow_info:
            unfollow_info.delete()
            return JsonResponse({'info': '成功取消关注'}, status=200)
        return JsonResponse({'error': '非法的操作'}, status=401)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# 移除粉丝
@authenticate_request
def remove_fans(request, payload):
    try:
        user_id = payload['user_id']
        fans_id = json.loads(request.body)['id']
        unfollow_info = Follows.objects.filter(fid=fans_id, lid=user_id).first()
        if unfollow_info:
            unfollow_info.delete()
            return JsonResponse({'info': '成功移除粉丝'}, status=200)
        return JsonResponse({'error': '非法的操作'}, status=401)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# 获取用户主页的个人信息
def query_user_index(request):
    try:
        data = json.loads(request.body)
        user_id = data.get('_id')
        if user_id and user_id != 'undefined':
            user = User.objects.filter(id=ObjectId(user_id)).first()
            if user:
                fans_count = Follows.objects.filter(lid=user_id).count()
                focus_count = Follows.objects.filter(fid=user_id).count()
                posts_count = Post.objects.filter(uid=user_id).count()
                author = {
                    'id': str(user.id),
                    'username': user.username,
                    'avatar': user.avatar,
                    'signature': user.signature,
                    'fans': fans_count,
                    'focusOn': focus_count,
                    'postsCount': posts_count,
                }
                return JsonResponse({'data': {'user': author}}, status=200)
            return JsonResponse({'error': '错误的访问'}, status=404)
        return JsonResponse({'error': '非法访问'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# 用户主页帖子
def query_user_index_post(request):
    try:
        type_mapping = {
            '帖子': 'posts',
            '点赞': 'favorites',
            '收藏': 'collected',
        }
        data = json.loads(request.body)
        user_id = data['user_id']
        types = data['types']
        offset = data['offset']
        user = User.objects.filter(id=ObjectId(user_id)).first()
        if user and types in type_mapping:
            field_name = type_mapping[types]
            postObj = []
            if field_name == 'posts':
                postObj = Post.objects.filter(uid=user_id)
            elif field_name == 'favorites':
                favorite_records = Favorites.objects.filter(uid=user_id)
                for favorite_record in favorite_records:
                    pid = favorite_record.pid
                    post = Post.objects.filter(id=ObjectId(pid)).first()
                    if post:
                        postObj.append(post)
            else:
                collect_records = Collects.objects.filter(uid=user_id)
                for collect_record in collect_records:
                    pid = collect_record.pid
                    post = Post.objects.filter(id=ObjectId(pid)).first()
                    if post:
                        postObj.append(post)
            posts = filter_querySet(postObj, offset, limit=10)
            if posts:
                return JsonResponse({'info': list(combine_index_post(posts))}, status=200)
            return JsonResponse({'info': []}, status=200)
        return JsonResponse({'error': '错误访问'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# 用户管理页面数据获取
@authenticate_request
def user_control_index(request, payload):
    try:
        user_id = payload['user_id']
        data = json.loads(request.body)
        offset = data['offset']
        types = data['types']
        user = User.objects.filter(id=ObjectId(user_id)).first()
        if user:
            user_data = []
            if types == 'posts':
                user_data = Post.objects.filter(uid=user_id)
                info = get_user_post_info(user_data, offset)
            elif types == 'collected':
                collect_records = Collects.objects.filter(uid=user_id)
                for collect_record in collect_records:
                    pid = collect_record.pid
                    post = Post.objects.filter(id=ObjectId(pid)).first()
                    if post:
                        user_data.append(post)
                info = get_user_post_info(user_data, offset)
            elif types == 'favorites':
                favorite_records = Favorites.objects.filter(uid=user_id)
                for favorite_record in favorite_records:
                    pid = favorite_record.pid
                    post = Post.objects.filter(id=ObjectId(pid)).first()
                    if post:
                        user_data.append(post)
                info = get_user_post_info(user_data, offset)
            elif types == 'fans':
                fan_records = Follows.objects.filter(lid=user_id)
                for fan_record in fan_records:
                    uid = fan_record.fid
                    fan = User.objects.filter(id=ObjectId(uid)).first()
                    if fan:
                        user_data.append(fan)
                info = get_user_info(user_data, offset)
            elif types == 'follow':
                follow_records = Follows.objects.filter(fid=user_id)
                for follow_record in follow_records:
                    uid = follow_record.lid
                    follow = User.objects.filter(id=ObjectId(uid)).first()
                    if follow:
                        user_data.append(follow)
                info = get_user_info(user_data, offset)
            else:
                return JsonResponse({'error': '错误的操作'}, status=404)
            total = len(user_data)
            return JsonResponse({'info': info, 'total': total}, status=200)
        return JsonResponse({'error': '错误的操作'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
