import datetime
import jwt
from django.http import JsonResponse
from jwt import exceptions
from .models import *
from web.settings import SECRET_KEY
from comment.models import *
from web.settings import TIME_ZONE
from post.utils import convert_to_timezone
from post.models import *
import os

def authenticate_request(view_func):
    def wrapper(request, *args, **kwargs):
        # 从请求中获取 JWT 令牌
        try:
            token = request.headers.get('Authorization').split(' ')[1]
            verify_payload = jwt.decode(token, SECRET_KEY, ['HS256'], verify=True)
            return view_func(request, verify_payload, *args, **kwargs)
        except exceptions.ExpiredSignatureError:
            error_message = {'error': '登录身份过期'}
            return JsonResponse(error_message, status=401)
        except jwt.DecodeError:
            error_message = {'error': 'jwt认证失败'}
            return JsonResponse(error_message, status=401)
        except jwt.InvalidTokenError:
            error_message = {'error': '非法的token'}
            return JsonResponse(error_message, status=401)
    return wrapper

def create_token(user):
    # 构造头部
    headers = {
        'typ': 'jwt',
        'alg': 'HS256',
    }
    # 构造payload
    payload = {
        'user_id': str(user._id),
        'username': user.username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=3600, days=5)  # 设置过期时间
    }
    result = jwt.encode(payload=payload, key=SECRET_KEY, algorithm='HS256', headers=headers)
    return result

# 检查邮箱
def check_email(email):
    user=User.objects.filter(email=email).first()
    if user:
        return True
    else:
        return False

# 整合主页帖子的信息
def combine_index_post(posts):
    for post in posts:
        img0=Image.objects.filter(pid=str(post._id)).first()
        image0_path=""
        image0_height,image0_width=0,0
        if img0:
            image0_path=img0.imagePath
            image0_height=img0.height
            image0_width=img0.width
        user=User.objects.filter(_id=ObjectId(post.uid)).first()
        info = {
            'title': post.title,
            'id': str(post._id),
            'img': image0_path,
            'img_info': {
                'height': image0_height,
                'width': image0_width,
            },
            'load': False,
            'user': {
                'id': str(user._id),
                'username': user.username,
                'avatar': user.avatar
            }
        }
        yield info

# 检查和删除图片，用于删除帖子时删除文件，以及删除用户上一次上传的头像
def check_and_delete(*, id, mainPath):
    # 获取目录下的文件
    file_list = os.listdir(mainPath)
    # 遍历文件列表，检查是否有对应的文件，如果有就删除
    for file_name in file_list:
        if file_name.startswith(f'{id}-'):
            file_path = os.path.join(mainPath, file_name)
            os.remove(file_path)

def filter_querySet(querySet, offset, limit=20):
    limit = limit  # 每页显示的帖子数量
    if isinstance(querySet, list):
        count = len(querySet)
    else:
        count = querySet.count()
    if 0 <= offset < count:
        start = offset
        end = offset + limit
        filterQuerySet = querySet.order_by('_id')[start:end]
        return filterQuerySet
    return []

def get_user_post_info(posts, offset):
    clear_posts = filter_querySet(posts, offset, 10)
    info = [{
        'date': convert_to_timezone(post.created_at, TIME_ZONE),
        'title': post.title,
        'likeCount': Favorites.objects.filter(pid=str(post._id)).count(),
        'collectCount': Collects.objects.filter(pid=str(post._id)).count(),
        'commentCount': Comment.objects.filter(pid=str(post._id)).count(),
        'content': post.content,
        'id': str(post._id),
        'username': User.objects.filter(_id=ObjectId(post.uid)).first().username,
    } for post in clear_posts if post]
    return info

def get_user_info(users, offset):
    clear_users = filter_querySet(users, offset, 10)
    info = [
        {
            'username': user.username,
            'avatar': user.avatar,
            'id': str(user._id),
            'fans': Follows.objects.filter(lid=str(user._id)).count(),
            'follow': Follows.objects.filter(fid=str(user._id)).count(),
            'note': Post.objects.filter(uid=str(user._id)).count()
        } for user in clear_users
    ]
    return info
