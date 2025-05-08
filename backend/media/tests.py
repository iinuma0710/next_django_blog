from io import BytesIO
from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient, APITestCase

from media.models import Image as ImageModel
from media.views import ImageUploadView


class TestImageUploadView(APITestCase):
    def _create_test_image(self, mode='RGB', size=(2000, 1000)):
        """ バッファ上にテスト用の画像を生成する関数 """
        img = Image.new(mode, size=(2000, 1000))
        byte_img = BytesIO()
        img.save(byte_img, 'jpeg')
        return byte_img.getvalue()

    def test_should_return_201(self):
        """ 画像ファイルを正常にアップロードできることをテストする関数 """
        # テスト用の画像ファイルを作成
        test_img = self._create_test_image()
        test_img_file = SimpleUploadedFile(name="test.jpg", content=test_img, content_type="image/jpeg")

        # 画像をアップロードする API を叩いてみる
        response = self.client.post(
            '/api/image/',
            {'title': 'Test Image', 'image': test_img_file},
            format='multipart'
        )

        # アップロードが成功することを確認する
        # 1. Status Code 201 が返ってくること
        self.assertEqual(response.status_code, 201)
        # 2. レスポンスのボディに画像のタイトルが入っていること
        self.assertEqual(response.data['title'], 'Test Image')
        # 3. レスポンスに、オリジナル、表示用、サムネイル用の３種類のフィールドが含まれていること
        self.assertIn('original_url', response.data)
        self.assertIn('display_url', response.data)
        self.assertIn('thumbnail_url', response.data)

    def test_should_return_400(self):
        """ アップロード時に title を指定しないとエラーになることを確認する関数 """
        # テスト用の画像ファイルを作成
        test_img = self._create_test_image()
        test_img_file = SimpleUploadedFile(name="test.jpg", content=test_img, content_type="image/jpeg")

        # リクエストボディに title を渡さない
        response = self.client.post(
            '/api/image/',
            {'image': test_img_file},
            format='multipart'
        )

        # アップロードが失敗することを確認する
        # 1. Status Code 400 が返ってくること
        self.assertEqual(response.status_code, 400)
        # 2. 所望のエラーメッセージが返ってくること
        self.assertEqual(response.data['error'], 'title and image file are required')