from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets, filters

from blog.models import Article
from blog.forms import ArticleForm
from blog.serializers import ArticleSerializer


def top(request):
    # ブログ記事を全件取得
    articles = Article.objects.all()
    # テンプレートエンジンに渡す Python オブジェクト
    context = {"articles": articles}
    return render(request, "articles/top.html", context)


@login_required
def article_new(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.created_by = request.user
            article.save()
            return redirect(article_detail, article_id=article.pk)
    else:
        form = ArticleForm()

    return render(request, "articles/article_new.html", {'form': form})


@login_required
def article_edit(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if article.created_by.id != request.user.id:
        return HttpResponseForbidden("この記事の編集はできません。")
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article_detail', article_id=article_id)
    else:
        form = ArticleForm(instance=article)

    return render(request, "articles/article_edit.html", {'form': form})


def article_detail(request, article_id):
    # article_id で指定された記事を取得、存在しない場合は 404 ページを返す
    article = get_object_or_404(Article, pk=article_id)
    return render(request, "articles/article_detail.html", {'article': article})


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('id', 'created_at',)
    ordering = ('created_at',)