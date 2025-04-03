from django.test import TestCase
from django.urls import resolve

from blog.views import top, article_new, article_edit, article_detail


class TopPageViewTest(TestCase):
    # トップページにアクセスしたときにステータスコード 200 が返ってくるか
    def test_top_returns_200(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    # トップページから返ってきたリクエストボディが b"Hello World!" か
    def test_top_returns_expected_content(self):
        response = self.client.get("/")
        self.assertEqual(response.content, b"Hello World!")


class CreateArticleTest(TestCase):
    def test_should_resolve_article_new(self):
        found = resolve("/articles/new/")
        self.assertEqual(article_new, found.func)


class ArticleDetailTest(TestCase):
    def test_should_resolve_article_detail(self):
        found = resolve("/articles/1/")
        self.assertEqual(article_detail, found.func)


class EditArticleTest(TestCase):
    def test_should_resolve_article_edit(self):
        found = resolve("/articles/1/edit")
        self.assertEqual(article_edit, found.func)