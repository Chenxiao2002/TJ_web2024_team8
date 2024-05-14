import web.post.models as models
import json

from django.shortcuts import render
from web.settings import SYSTEM_PATH
from django.http import JsonResponse
from django.db.models import Q
from PIL import Image

# Create your views here.
TIME_ZONE='Asia/Shanghai'

#以下是一些功能函数（util）
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
# 更换时区
def convert_to_timezone(datetime_obj, timezone_str):
    target_timezone = pytz.timezone(timezone_str)
    converted_datetime = datetime_obj.astimezone(target_timezone)
    return converted_datetime.strftime('%Y-%m-%d %H:%M')
def filter_querySet(querySet, offset, limit=20):
    limit = limit  # 每页显示的帖子数量
    count = querySet.count()
    if 0 <= offset < count:
        start = offset
        end = offset + limit
        filterQuerySet = querySet.order_by('-id')[start:end]
        return filterQuerySet
    return []
# 整合主页帖子的信息
def combine_index_post(posts):
    for post in posts:
        imgs = post.imgs.all()
        info = {
            'title': post.title,
            'id': post.id,
            'img': imgs[0].imagePath,
            'img_info': {
                'height': imgs[0].height,
                'width': imgs[0].width,
            },
            'load': False,
            'user': {
                'id': post.user.id,
                'username': post.user.username,
                'avatar': post.user.avatar
            }
        }
        yield info

#以下是POST的视图函数们
@authenticate_request
def upload_post(request, payload):
    file = request.FILES['file']
    id = request.POST.get('id')
    file_path = SYSTEM_PATH + 'post/' + str(id) + '-' + file.name
    with Image.open(file) as img:
        image_height = img.height
        image_width = img.width
    with open(file_path, 'wb') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    result = {
        'filename': file.name,
        'filepath': 'http://localhost:8000/static/img/post/' + str(id) + '-' + file.name,
    }
    post = models.Post.objects.filter(id=id).first()
    if post:
        models.Image.objects.create(imagePath=result['filepath'], post=post, height=image_height, width=image_width)
        return JsonResponse({'data': 'success'}, status=200)
    return JsonResponse({'error': '错误的操作'}, status=401)

# 用户上传帖子
@authenticate_request
def upload_post_info(request, payload):
    data = json.loads(request.body)
    post = models.Post.objects.create(
        title=data.get('title'),
        content=data.get('content'),
        user_id=data.get('user_id')
    )
    return JsonResponse({'data': 'success', 'info': post.id}, status=200)

# 获取帖子详情，整合信息
def get_post_detail(request):
    data = json.loads(request.body)
    id = data.get('id')
    post = models.Post.objects.filter(id=id).first()
    if post:
        imgs = post.imgs.all()
        info = {
            'title': post.title,
            'id': post.id,
            'imgs': [img.imagePath for img in imgs],
            'user': {
                'id': post.user.id,
                'username': post.user.username,
                'avatar': post.user.avatar
            },
            'createTime': convert_to_timezone(post.created_at, TIME_ZONE),
            'likeCount': post.favoritePosts.count(),
            'collectCount': post.collectedPosts.count(),
            'commentCount': post.comments.count(),
            'content': post.content
        }
        return JsonResponse({'info': info}, status=200)
    return JsonResponse({'error': '错误的访问'}, status=404)

# 主页推送帖子
def query_post_index(request):
    data = json.loads(request.body)
    offset = data['offset']
    query = data.get('query')
    if query:
        posts = models.Post.objects.filter(
            Q(title__icontains=query) |
            Q(user__username__icontains=query) |
            Q(content__icontains=query)
        )
    else:
        posts = models.Post.objects
    posts = filter_querySet(posts, offset, limit=10)
    if posts:
        return JsonResponse({'info': list(combine_index_post(posts))}, status=200)
    # 没有内容了
    return JsonResponse({'info': []}, status=200)

@authenticate_request
def control_like_collect(request, payload):
    user_id = payload['user_id']
    data = json.loads(request.body)
    operation = data['operator']
    post_id = data['post_id']
    types = data['type']
    user = models.User.objects.filter(id=user_id).first()
    post = models.Post.objects.filter(id=post_id).first()
    if user and post:
        if types == 'like':
            if not operation:
                user.favorites.add(post)
                return JsonResponse({'info': '成功添加喜欢'}, status=200)
            user.favorites.remove(post)
            return JsonResponse({'info': '成功取消喜欢'}, status=200)
        elif types == 'collect':
            if not operation:
                user.collected.add(post)
                return JsonResponse({'info': '成功添加收藏'}, status=200)
            user.collected.remove(post)
            return JsonResponse({'info': '成功取消收藏'}, status=200)
    return JsonResponse({'error': '错误的操作'}, status=404)


@authenticate_request
def post_delete(request, payload):
    data = json.loads(request.body)
    id = data['id']
    post = models.Post.objects.filter(id=id).first()
    if post:
        if post.user.id == payload['user_id']:
            post.delete()
            return JsonResponse({'success': '帖子删除成功'}, status=200)
        return JsonResponse({'error': '错误'}, status=401)
    return JsonResponse({'error': '错误'}, status=401)
