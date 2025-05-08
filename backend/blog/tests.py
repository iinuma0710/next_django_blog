from django.test import TestCase, Client, RequestFactory
from django.urls import resolve
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from blog.models import Article
from blog.views import (
    top,
    article_new,
    article_edit,
    article_detail,
    ArticleViewSet,
)

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


class ArticleViewSetTest(APITestCase):
    def setUp(self):
        self.user = UserModel.objects.create(
            username="test_user",
            email="test@example.com",
            password="top_secret_pass0001",
        )
        self.article_1 = Article.objects.create(
            title="title_1",
            abstract="abstract_1",
            body="body_1",
            created_by=self.user
        )
        self.article_2 = Article.objects.create(
            title="title_2",
            abstract="abstract_2",
            body="body_2",
            created_by=self.user
        )

    def test_list_article(self):
        # 記事の一覧を取得する
        response = self.client.get('/api/articles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK) # 記事の全件取得に成功すること
        self.assertEqual(len(response.data), 2)     # 取得できたデータは２件あること

    def test_create_article(self):
        # 記事を新規作成する
        new_article = {'title': 'タイトル', 'abstract': '概要', 'body': '本文', 'created_by': 1}
        response = self.client.post('/api/articles/', new_article)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) # 記事の作成に成功すること
        self.assertEqual(response.data['title'], 'タイトル')             # 作成した記事のタイトルが期待通りであること


    def test_retrieve_article(self):
        # 指定した ID の記事を取得する
        response = self.client.get('/api/articles/1/')   # ID = 1 の記事を取得する
        self.assertEqual(response.status_code, status.HTTP_200_OK) # 記事の詳細取得に成功すること
        self.assertEqual(response.data['title'], 'title_1')        # 所望の記事のタイトルが得られていること

    def test_update_article(self):
        # 指定した記事を更新する
        updated_article = {
            'title': self.article_1.title,
            'abstract': 'updated abstract',
            'body': 'updated body',
            'created_by': self.user.id
        }
        response = self.client.patch('/api/articles/1/', updated_article)
        self.assertEqual(response.status_code, status.HTTP_200_OK) # 記事の作成に成功すること
        self.assertEqual(response.data['abstract'], 'updated abstract') # 更新した記事の概要が期待通りであること
        self.assertEqual(response.data['body'], 'updated body')         # 更新した記事の本文が期待通りであること


    def test_delete_article(self):
        # 指定した ID の記事を削除する
        response = self.client.delete('/api/articles/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)      # 削除が成功すること
        self.assertFalse(Article.objects.filter(pk=self.article_1.pk).exists()) # 指定した ID の記事が存在しないこと