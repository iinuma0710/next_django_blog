from django.test import TestCase, Client, RequestFactory
from django.urls import resolve
from django.contrib.auth import get_user_model

from blog.models import Article
from blog.views import top, article_new, article_edit, article_detail

UserModel = get_user_model()


class TopPageTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create(
            username="test_user",
            email="test@example.com",
            password="top_secret_pass0001",
        )
        self.article = Article.objects.create(
            title="title1",
            abstract="abstract",
            body="body",
            created_by=self.user
        )

    def test_should_return_article_title(self):
        request = RequestFactory().get("/")
        request.user = self.user
        response = top(request)
        self.assertContains(response, self.article.title)

    def test_should_return_username(self):
        request = RequestFactory().get("/")
        request.user = self.user
        response = top(request)
        self.assertContains(response, self.user.username)


class CreateArticleTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create(
            username="test_user",
            email="test@example.com",
            password="top_secret_pass0001",
        )
        self.client.force_login(self.user)

    def test_render_creation_form(self):
        response = self.client.get("/articles/new/")
        self.assertContains(response, "ブログ記事の新規作成", status_code=200)
    
    def test_create_article(self):
        data = {'title': 'タイトル', 'abstract': '概要', 'body': '本文'}
        self.client.post('/articles/new/', data)
        article = Article.objects.get(title='タイトル')
        self.assertEqual('概要', article.abstract)
        self.assertEqual('本文', article.body)


class ArticleDetailTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create(
            username="test_user",
            email="test@example.com",
            password="top_secret_pass0001",
        )
        self.article = Article.objects.create(
            title="title1",
            abstract="abstract",
            body="body",
            created_by=self.user
        )

    def test_should_use_expected_template(self):
        response = self.client.get("/articles/%s/" % self.article.id)
        self.assertTemplateUsed(response, "articles/article_detail.html")
    
    def test_should_return_200_and_expected_heading(self):
        response = self.client.get("/articles/%s/" % self.article.id)
        self.assertContains(response, self.article.title, status_code=200)


# class EditArticleTest(TestCase):
#     def test_should_resolve_article_edit(self):
#         found = resolve("/articles/1/edit")
#         self.assertEqual(article_edit, found.func)