import json
from django.db.models import Count
from django.http import JsonResponse
from .models import Comment
from user.models import User
from user.utils import filter_querySet,authenticate_request
from post.utils import convert_to_timezone
from web.settings import TIME_ZONE
from bson import ObjectId

#发布评论
@authenticate_request 
def do_comment(request, verify_payload):
    data = json.loads(request.body)
    user_id = verify_payload['user_id']
    post_id = data['post_id']
    content = data['content']
    if 'parent_comment_id' in data:
        parent_cid=data['parent_comment_id']
    else:
        parent_cid='#'
    comment = Comment.objects.create(uid=user_id,pid=post_id,content=content,parent_cid=parent_cid)
    return JsonResponse({'info': '评论已发送！', 'id': str(comment._id)}, status=200)

#获取主评
def get_comment(request):
    data = json.loads(request.body)
    post_id = data['id']
    offset = data['offset']
    comments = Comment.objects.filter(pid=post_id, parent_cid='#')
    filter_comments = filter_querySet(comments, offset, limit=5)
    if filter_comments:
        data=[]
        for comment in filter_comments:
            if comment:
                user=User.objects.filter(_id=ObjectId(comment.uid)).first()
                reply_count=Comment.objects.filter(parent_cid=str(comment._id)).count()
                comment_data={
                    'id': str(comment._id),
                    'content': comment.content,
                    'createTime': convert_to_timezone(comment.created_at, TIME_ZONE),
                    'user': {
                        'id': comment.uid,
                        'username': user.username,
                        'avatar': user.avatar
                    },
                    'replyCount': reply_count,
                    'replies': []
                }
                data.append(comment_data)
        return JsonResponse({'info': data}, status=200)
    return JsonResponse({'info': []}, status=200)

#获取子评
def load_reply(request):
    data = json.loads(request.body)
    id = data['id']
    offset = data['offset']
    comment = Comment.objects.filter(_id=ObjectId(id)).first()
    if comment:
        replies = Comment.objects.filter(parent_cid=str(comment._id))
        filter_replies = filter_querySet(replies, offset, limit=5)
        data=[]
        for reply in filter_replies:
            if reply:
                user=User.objects.filter(_id=ObjectId(reply.uid)).first()
                reply_data={
                    'id': str(reply._id),
                    'content': reply.content,
                    'createTime': convert_to_timezone(reply.created_at, TIME_ZONE),
                    'user': {
                        'id': str(user._id),
                        'username': user.username,
                        'avatar': user.avatar
                    },
                }
                data.append(reply_data)
        return JsonResponse({'info': data, 'count': len(data)}, status=200)
    return JsonResponse({'error': '错误的操作'}, status=404)