import json
import string
import random
import time
from .models import *
from .utils import *
from web.settings import BASE_DIR,TIME_ZONE
from bson import ObjectId
from django.views.decorators.http import require_http_methods
from bson import json_util

@authenticate_request
def getAllUsers(request, payload):
    user_id = payload['user_id']
    user=User.objects.filter(_id=ObjectId(user_id)).first()
    if user and user.status==0:
        u_list=User.objects.all()
        user_list=[]
        for u in u_list:
            user_data={
                'id': str(u._id),
                'username':u.username,
                'status':u.status
            }
            user_list.append(user_data)
        return JsonResponse({'info': user_list}, status=200)
    else:
        return JsonResponse({'error':'非管理员用户'}, status=400)

@authenticate_request
def block(request, payload):
    user_id = payload['user_id']
    user=User.objects.filter(_id=ObjectId(user_id)).first()
    if user and user.status==0:
        blocked_uid=json.loads(request.body).get('id')
        blocked_user=User.objects.filter(_id=ObjectId(blocked_uid)).first()
        if blocked_user:
            blocked_user.status=2
            blocked_user.save()
            return JsonResponse({'info': '拉黑用户成功'}, status=200)
        return JsonResponse({'error':'拉黑用户不存在'}, status=401)
    else:
        return JsonResponse({'error':'非管理员用户'}, status=400)

@authenticate_request
def unblock(request, payload):
    user_id = payload['user_id']
    user=User.objects.filter(_id=ObjectId(user_id)).first()
    if user and user.status==0:
        unblocked_uid=json.loads(request.body).get('id')
        unblocked_user=User.objects.filter(_id=ObjectId(unblocked_uid)).first()
        if unblocked_user:
            if unblocked_user.status==2:
                unblocked_user.status=1
                unblocked_user.save()
                return JsonResponse({'info': '取消拉黑用户成功'}, status=200)
            return JsonResponse({'error':'用户非拉黑状态'}, status=200)
        return JsonResponse({'error':'取消拉黑用户不存在'}, status=401)
    else:
        return JsonResponse({'error':'非管理员用户'}, status=400)

@authenticate_request
def set_admin(request,payload):
    user_id=payload['user_id']
    user=User.objects.filter(_id=ObjectId(user_id)).first()
    data=json.loads(request.body)
    set_uid=data.get('id')
    set_user=User.objects.filter(_id=ObjectId(set_uid)).first()
    if user and user.status==0:
        if set_user:
            set_user.status=0
            set_user.save()
            return JsonResponse({'info':'成功任命管理员'},status=200)
        return JsonResponse({'error':'此用户不存在'},status=401)        
    return JsonResponse({'error':'无权限'},status=400)

