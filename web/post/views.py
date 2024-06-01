import json
from PIL import Image as PIL_Image
from django.db.models import Q
from django.http import JsonResponse
from .models import Post
from user.models import *
from comment.models import Comment
from .utils import convert_to_timezone
from user.utils import combine_index_post, filter_querySet,authenticate_request
from web.settings import TIME_ZONE, SYSTEM_PATH
from bson import ObjectId

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
        posts = Post.objects
    posts = filter_querySet(posts, offset, limit=10)
    if posts:
        return JsonResponse({'info': list(combine_index_post(posts))}, status=200)
    return JsonResponse({'info': []}, status=200)

# 获取帖子详情，整合信息
def get_post_detail(request):
    data = json.loads(request.body)
    id = data.get('id')
    post = Post.objects.filter(_id=ObjectId(id)).first()
    if post:
        imgs = Image.objects.filter(pid=str(post._id))
        user = User.objects.filter(_id=ObjectId(post.uid)).first()
        info = {
            'title': post.title,
            'id': str(post._id),
            'imgs': [img.imagePath for img in imgs],
            'user': {
                'id': str(user._id),
                'username': user.username,
                'avatar': user.avatar
            },
            'createTime': convert_to_timezone(post.created_at, TIME_ZONE),
            'likeCount': Favorites.objects.filter(pid=str(post._id)).count(),
            'collectCount': Collects.objects.filter(pid=str(post._id)).count(),
            'commentCount': Comment.objects.filter(pid=str(post._id)).count(),
            'content': post.content
        }
        return JsonResponse({'info': info}, status=200)
    return JsonResponse({'error': '错误的访问'}, status=404)

#删除帖子
@authenticate_request
def post_delete(request, payload):
    data = json.loads(request.body)
    id = data['id']
    post = Post.objects.filter(_id=ObjectId(id)).first()
    if post:
        if post.uid == payload['user_id']:
            post.delete()
            return JsonResponse({'success': '帖子删除成功'}, status=200)
        return JsonResponse({'error': '错误'}, status=401)
    return JsonResponse({'error': '错误'}, status=401)

#点赞收藏控制
@authenticate_request
def control_like_collect(request, payload):
    user_id = payload['user_id']
    data = json.loads(request.body)
    operation = data['operator']
    post_id = data['post_id']
    operation_type = data['type']
    user = User.objects.filter(_id=ObjectId(user_id)).first()
    post = Post.objects.filter(_id=ObjectId(post_id)).first()
    if user and post:
        if operation_type == 'like':
            if not operation:
                Favorites.objects.create(uid=user_id,pid=post_id)
                return JsonResponse({'info': '成功添加喜欢'}, status=200)
            Favorites.objects.filter(uid=user_id,pid=post_id).first().delete()
            return JsonResponse({'info': '成功取消喜欢'}, status=200)
        elif operation_type == 'collect':
            if not operation:
                Collects.objects.create(uid=user_id,pid=post_id)
                return JsonResponse({'info': '成功添加收藏'}, status=200)
            Collects.objects.filter(uid=user_id,pid=post_id).first().delete()
            return JsonResponse({'info': '成功取消收藏'}, status=200)
    return JsonResponse({'error': '错误的操作'}, status=404)

# 用户上传帖子
@authenticate_request
def upload_post_info(request, payload):
    data = json.loads(request.body)
    post = Post.objects.create(
        title=data.get('title'),
        content=data.get('content'),
        uid=data.get('user_id')
    )
    return JsonResponse({'data': 'success', 'info': str(post._id)}, status=200)

#帖子上传图片
@authenticate_request
def upload_post(request, payload):
    file = request.FILES['file']
    id = request.POST.get('id')
    file_path = SYSTEM_PATH + 'post/' + str(id) + '-' + file.name
    with PIL_Image.open(file) as img:
        image_height = img.height
        image_width = img.width
    with open(file_path, 'wb') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    result = {
        'filename': file.name,
        'filepath': 'http://localhost:8000/static/img/post/' + str(id) + '-' + file.name,
    }
    post = Post.objects.filter(_id=ObjectId(id)).first()
    if post:
        Image.objects.create(imagePath=result['filepath'], pid=id, height=image_height, width=image_width)
        return JsonResponse({'data': 'success'}, status=200)
    return JsonResponse({'error': '错误的操作'}, status=401)


