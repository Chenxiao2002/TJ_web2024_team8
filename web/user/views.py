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
#from .forms import LoginForm, RegForm, ChangeNicknameForm, BindEmailForm, ChangePasswordForm, ForgotPasswordForm
from .models import User
#from blog.models import Blog,BlogType
from django.core.paginator import Paginator
from .utils import *
from web.settings import BASE_DIR

IMG_DIR=BASE_DIR/'img' #需要最后确定头像存储路径，先瞎编一个

# 用户登录
def login(request):
    data = json.loads(request.body)
    user = User.objects.filter(**data).first()
    if user:
        token = create_token(user)
        user = {
            'id': user.id,
            'username': user.username,
            'avatar': user.avatar,
            'signature': user.signature,
            'token': token
        }
        return JsonResponse(user, status=200)
    error_message = {'error': '邮箱或密码错误'}
    return JsonResponse(error_message, status=401)


# 用户注册
def register(request):
    data = json.loads(request.body)
    email = data['email']
    if check_email(email):
        return JsonResponse({'error': '该邮箱已被注册'}, status=401)
    try:
        User.objects.create(**data)
        return JsonResponse({'info': '创建用户成功'})
    except Exception as e:
        print(e)
        return JsonResponse({'error': '创建用户失败'}, status=401)


# 获取用户主页的个人信息
def query_user_index(request):
    data = json.loads(request.body)
    if data.get('id') and data.get('id') != 'undefined':
        user = User.objects.filter(id=data.get('id')).first()
        if user:
            author = {
                'id': user.id,
                'username': user.username,
                'avatar': user.avatar,
                'signature': user.signature,
                'fans': user.beFocusOn.count(),
                'focusOn': user.following.count(),
                'postsCount': user.posts.count(),
            }
            info = {
                'user': author,
            }
            return JsonResponse({'data': info}, status=200)
        return JsonResponse({'error': '错误的访问'}, status=404)
    return JsonResponse({'error': '非法访问'}, status=404)


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
    user = User.objects.filter(id=user_id).first()
    if user and types in type_mapping:
        field_name = type_mapping[types]
        postObj = getattr(user, field_name)
        posts = filter_querySet(postObj, offset, limit=10)
        if posts:
            return JsonResponse({'info': list(combine_index_post(posts))}, status=200)
        return JsonResponse({'info': []}, status=200)
    return JsonResponse({'error': '错误访问'}, status=404)


# 获取用户关注用户id
@authenticate_request
def get_user_focus(request, payload):
    user_id = payload['user_id']
    user = User.objects.filter(id=user_id).first()
    following = user.following.all()
    ids = [u.id for u in following]
    collected = user.collected.all()
    c_ids = [u.id for u in collected]
    favorites = user.favorites.all()
    f_ids = [u.id for u in favorites]
    return JsonResponse({'info': {
        'follow': ids, 'collected': c_ids, 'favorites': f_ids
    }}, status=200)


# 用户关注
@authenticate_request
def focusOn(request, payload):
    # 做关注操作的用户id
    id1 = payload['user_id']
    user1 = User.objects.filter(id=id1).first()
    # 被关注的用户id
    id2 = json.loads(request.body)['id']
    user2 = User.objects.filter(id=id2).first()
    if user1 and user2:
        user1.following.add(user2)
        return JsonResponse({'info': '成功关注'}, status=200)
    return JsonResponse({'error': '非法的操作'}, status=401)


@authenticate_request
def unfollow(request, payload):
    # 取消关注操作的用户id
    user_id = payload['user_id']
    user = User.objects.filter(id=user_id).first()
    # 被取消关注的用户id
    unfollow_id = json.loads(request.body)['id']
    unfollow_user = User.objects.filter(id=unfollow_id).first()
    if user and unfollow_user:
        user.following.remove(unfollow_user)
        return JsonResponse({'info': '成功取消关注'}, status=200)
    return JsonResponse({'error': '非法的操作'}, status=401)


@authenticate_request
def remove_fans(request, payload):
    # 移除操作的用户id
    user_id = payload['user_id']
    user = User.objects.filter(id=user_id).first()
    # 移除的粉丝id
    fans_id = json.loads(request.body)['id']
    fan = User.objects.filter(id=fans_id).first()
    if user and fan:
        fan.following.remove(user)
        return JsonResponse({'info': '成功移除粉丝'}, status=200)
    return JsonResponse({'error': '非法的操作'}, status=401)


@authenticate_request
def update_user_info(request, payload):
    data = json.loads(request.body)
    user_id = payload['user_id']
    user = User.objects.filter(id=user_id).first()
    user.username = data['username']
    user.signature = data['signature']
    user.save()
    return JsonResponse({'info': '修改成功'}, status=200)


@authenticate_request
def update_avatar(request, payload):
    file = request.FILES['file']
    id = payload['user_id']
    file_path = SYSTEM_PATH + 'avatar/' + str(id) + '-' + file.name
    check_and_delete(id=id, mainPath=SYSTEM_PATH + 'avatar/')
    with open(file_path, 'wb') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    result = {
        'filename': file.name,
        'filepath': 'http://localhost:8000/static/img/avatar/' + str(id) + '-' + file.name,
    }
    user = User.objects.filter(id=id).first()
    user.avatar = 'http://localhost:8000/static/img/avatar/' + str(id) + '-' + file.name
    user.save()
    return JsonResponse({'info': result}, status=200)


@authenticate_request
def user_control_index(request, payload):
    user_id = payload['user_id']
    data = json.loads(request.body)
    offset = data['offset']
    types = data['types']
    user = User.objects.filter(id=user_id).first()
    if user:
        if types == 'posts':
            user_data = user.posts
            info = get_user_post_info(user_data, offset)
        elif types == 'collected':
            user_data = user.collected
            info = get_user_post_info(user_data, offset)
        elif types == 'favorites':
            user_data = user.favorites
            info = get_user_post_info(user_data, offset)
        elif types == 'fans':
            user_data = user.beFocusOn
            info = get_user_info(user_data, offset)
        elif types == 'follow':
            user_data = user.following
            info = get_user_info(user_data, offset)
        else:
            return JsonResponse({'error': '错误的操作'}, status=404)
        total = user_data.count()
        return JsonResponse({'info': info, 'total': total}, status=200)
    return JsonResponse({'error': '错误的操作'}, status=404)


# def user_info(request):
#     user=request.user
#     if not user.is_authenticated:
#         return redirect(request.GET.get('from', reverse('home')))
#     my_all_blogs=Blog.objects.filter(author=request.user)
#     paginator = Paginator(my_all_blogs, 10)
#     page_num = request.GET.get('page', 1) # 获取url的页面参数（GET请求）
#     page_of_blogs = paginator.get_page(page_num)
#     context = {}
#     context['my_all_blogs'] = my_all_blogs
#     context['page_of_blogs'] = page_of_blogs  
#     return render(request, 'user/user_info.html', context)


# def login_for_medal(request):
#     login_form = LoginForm(request.POST)
#     data = {}
#     if login_form.is_valid():
#         user = login_form.cleaned_data['user']
#         auth.login(request, user)
#         data['status'] = 'SUCCESS'
#     else:
#         data['status'] = 'ERROR'
#     return JsonResponse(data)

# def login(request):
#     if request.method == 'POST':
#         login_form = LoginForm(request.POST)
#         if login_form.is_valid():
#             user = login_form.cleaned_data['user']
#             auth.login(request, user)
#             return redirect(request.GET.get('from', reverse('home')))
#     else:
#         login_form = LoginForm()

#     context = {}
#     context['login_form'] = login_form
#     return render(request, 'user/login.html', context)

# def register(request):
#     if request.method == 'POST':
#         reg_form = RegForm(request.POST, request=request)
#         if reg_form.is_valid():
#             username = reg_form.cleaned_data['username']
#             email = reg_form.cleaned_data['email']
#             password = reg_form.cleaned_data['password']
#             # 创建用户
#             user = User.objects.create_user(username, email, password)
#             user.save()
#             # 清除session
#             del request.session['register_code']
#             # 登录用户
#             user = auth.authenticate(username=username, password=password)
#             auth.login(request, user)
#             return redirect(request.GET.get('from', reverse('home')))
#     else:
#         reg_form = RegForm()

#     context = {}
#     context['reg_form'] = reg_form
#     return render(request, 'user/register.html', context)
    
# def logout(request):
#     auth.logout(request)
#     return redirect(request.GET.get('from', reverse('home')))



# def change_nickname(request):
#     redirect_to = request.GET.get('from', reverse('home'))

#     if request.method == 'POST':
#         form = ChangeNicknameForm(request.POST, user=request.user)
#         if form.is_valid():
#             nickname_new = form.cleaned_data['nickname_new']
#             profile, created = Profile.objects.get_or_create(user=request.user)
#             profile.nickname = nickname_new
#             profile.save()
#             return redirect(redirect_to)
#     else:
#         form = ChangeNicknameForm()

#     context = {}
#     context['page_title'] = '修改昵称'
#     context['form_title'] = '修改昵称'
#     context['submit_text'] = '修改'
#     context['form'] = form
#     context['return_back_url'] = redirect_to
#     return render(request, 'form.html', context)

# def bind_email(request):
#     redirect_to = request.GET.get('from', reverse('home'))

#     if request.method == 'POST':
#         form = BindEmailForm(request.POST, request=request)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             request.user.email = email
#             request.user.save()
#             # 清除session
#             del request.session['bind_email_code']
#             return redirect(redirect_to)
#     else:
#         form = BindEmailForm()

#     context = {}
#     context['page_title'] = '绑定邮箱'
#     context['form_title'] = '绑定邮箱'
#     context['submit_text'] = '绑定'
#     context['form'] = form
#     context['return_back_url'] = redirect_to
#     return render(request, 'user/bind_email.html', context)

# def send_verification_code(request):
#     email = request.GET.get('email', '')
#     send_for = request.GET.get('send_for', '')
#     data = {}

#     if email != '':
#         # 生成验证码
#         code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
#         now = int(time.time())
#         send_code_time = request.session.get('send_code_time', 0)
#         if now - send_code_time < 30:
#             data['status'] = 'ERROR'
#         else:
#             request.session[send_for] = code
#             request.session['send_code_time'] = now
            
#             # 发送邮件
#             send_mail(
#                 '绑定邮箱',
#                 '验证码：%s' % code,
#                 '1376908007@qq.com',
#                 [email],
#                 fail_silently=False,
#             )
#             data['status'] = 'SUCCESS'
#     else:
#         data['status'] = 'ERROR'
#     return JsonResponse(data)

# def change_password(request):
#     redirect_to = reverse('home')
#     if request.method == 'POST':
#         form = ChangePasswordForm(request.POST, user=request.user)
#         if form.is_valid():
#             user = request.user
#             old_password = form.cleaned_data['old_password']
#             new_password = form.cleaned_data['new_password']
#             user.set_password(new_password)
#             user.save()
#             auth.logout(request)
#             return redirect(redirect_to)
#     else:
#         form = ChangePasswordForm()

#     context = {}
#     context['page_title'] = '修改密码'
#     context['form_title'] = '修改密码'
#     context['submit_text'] = '修改'
#     context['form'] = form
#     context['return_back_url'] = redirect_to
#     return render(request, 'form.html', context)

# def forgot_password(request):
#     redirect_to = reverse('login')
#     if request.method == 'POST':
#         form = ForgotPasswordForm(request.POST, request=request)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             new_password = form.cleaned_data['new_password']
#             user = User.objects.get(email=email)
#             user.set_password(new_password)
#             user.save()
#             # 清除session
#             del request.session['forgot_password_code']
#             return redirect(redirect_to)
#     else:
#         form = ForgotPasswordForm()

#     context = {}
#     context['page_title'] = '重置密码'
#     context['form_title'] = '重置密码'
#     context['submit_text'] = '重置'
#     context['form'] = form
#     context['return_back_url'] = redirect_to
#     return render(request, 'user/forgot_password.html', context)