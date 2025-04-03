from django.http import HttpResponse


def top(request):
    return HttpResponse(b"Hello World!")


def article_new(request):
    return HttpResponse('ブログ記事の新規作成')


def article_edit(request):
    return HttpResponse('ブログ記事の編集')


def article_detail(request):
    return HttpResponse('ブログ記事の詳細表示')
