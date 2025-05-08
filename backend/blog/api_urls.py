from django.urls import path
from blog import api_views

article_list = api_views.ArticleViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

article_detail = api_views.ArticleViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('', article_list, name='article-list'),
    path('<int:pk>/', article_detail, name='article-detail'),
]