from django.db import models

# Create your models here.
class Image(models.Model):
    title = models.CharField('画像タイトル', max_length=128)
    thumbnail_url = models.CharField('サムネイル画像の URL', max_length=256)
    display_url = models.CharField('表示用画像の URL', max_length=256)
    original_url = models.CharField('オリジナル画像の URL', max_length=256)
    uploaded_at = models.DateTimeField('アップロード日時', auto_now_add=True)

    def __str__(self):
        return self.title