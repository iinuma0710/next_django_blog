from rest_framework import viewsets, filters

from blog.models import Article
from blog.serializers import ArticleSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('id', 'created_at',)
    ordering = ('created_at',)
