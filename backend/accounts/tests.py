import jwt
from django.conf import settings
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse

from accounts.models import CustomUser


class TokenObtainTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            username='test_user',
            password='test_password',
            is_staff=True,
            is_superuser=False,
        )
        self.token_url = reverse('token_obtain_pair')

    def test_toke_obtain_success(self):
        response = self.client.post(
            self.token_url,
            {
                'email': 'test@example.com',
                'password': 'test_password',
            },
            format='json'
        )

        # 200 のステータスコードと access、refresh トークンが発行されることを確認
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

        # トークンをデコードして user_id、is_staff、is_superuser がトークンに含まれていることを確認
        access_token = response.data['access']
        decoded = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
        self.assertEqual(decoded['user_id'], self.user.id)
        self.assertEqual(decoded['is_staff'], self.user.is_staff)
        self.assertEqual(decoded['is_superuser'], self.user.is_superuser)

    def test_token_obtain_fail(self):
        response = self.client.post(
            self.token_url,
            {
                'email': 'test@example.com',
                'password': 'wrong_password',
            },
            format='json'
        )

        # パスワードが間違っているので、401 のステータスコードが返ってくることを確認
        self.assertEqual(response.status_code, 401)
        self.assertNotIn('access', response.data)
        self.assertNotIn('refresh', response.data)


class TokenRefreshTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            username='test_user',
            password='test_password',
            is_staff=True,
            is_superuser=False,
        )
        self.refresh_token = RefreshToken.for_user(self.user)
        self.refresh_url = reverse('token_refresh')

    def test_refresh_token_success(self):
        response = self.client.post(
            self.refresh_url,
            {
                'refresh': str(self.refresh_token),
            },
            format='json'
        )

        # ステータスコード 200 とアクセストークンが返ってくること
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)

        # トークンをデコードして user_id、is_staff、is_superuser がトークンに含まれていることを確認
        access_token = response.data['access']
        decoded = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
        self.assertEqual(decoded['user_id'], self.user.id)
        self.assertEqual(decoded['is_staff'], self.user.is_staff)
        self.assertEqual(decoded['is_superuser'], self.user.is_superuser)