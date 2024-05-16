# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.contrib.auth.models import User as BaseUser
# from .models import User


# class UserAdmin(BaseUserAdmin):
#     list_display = ('username', 'nickname', 'email', 'is_staff', 'is_active', 'is_superuser', 'level')
#     fieldsets = (
#         (None, {'fields': ('username', 'password')}),
#         ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'avatar', 'signature', 'nickname', 'level')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#         ('Important dates', {'fields': ('last_login', 'date_joined')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'email', 'password1', 'password2'),
#         }),
#         ('Personal Info', {'fields': ('nickname', 'avatar', 'signature', 'level')}),
#     )

# # 注销旧的 UserAdmin，如果已经注册过的话
# admin.site.unregister(BaseUser)
# # 重新注册更新后的 UserAdmin
# admin.site.register(User, UserAdmin)