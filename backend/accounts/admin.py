from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    # 一覧画面にの表示する項目
    list_display = ('email', 'username', 'is_superuser', 'is_staff', 'is_active')
    
    # 一覧画面で絞り込める項目
    list_filter = ('is_superuser', 'is_staff', 'is_active')

    # 既存レコードで表示するフィールド
    fieldsets = [
        ('メールアドレス', {'fields': ('email', )}),
        ('ユーザ名', {'fields': ('username', )}),
        ('ユーザ権限', {'fields': ('is_superuser', 'is_staff', 'is_active')}),
        ('個人設定', {'fields': ('profile_image', 'bio')}),
    ]

    # 新規作成画面で表示するフィールド
    add_fieldsets = [
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
        }),
    ]


admin.site.register(CustomUser, CustomUserAdmin)