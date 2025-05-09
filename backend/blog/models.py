from django.conf import settings
from django.db import models


class Article(models.Model):
    title = models.CharField('記事タイトル', max_length=128)
    abstract = models.TextField('記事概要', blank=True)
    body = models.TextField('記事本文', blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='投稿者',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField("投稿日", auto_now_add=True)
    updated_at = models.DateTimeField("更新日", auto_now=True)

    def __str__(self):
        return self.title
