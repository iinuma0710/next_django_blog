from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField("投稿日", auto_now_add=True)
    updated_at = models.DateTimeField("更新日", auto_now=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.TextField('略歴', blank=True)

    # 不要なフィールドは無効にしておく
    first_name = None
    last_name = None
    date_joined = None

    # ログインにはメールアドレスを利用する
    USERNAME_FIELD = 'email'
    # ユーザ名とメールアドレスの設定は必須
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username