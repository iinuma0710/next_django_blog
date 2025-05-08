import uuid
from PIL import Image
from io import BytesIO

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Image as ImageModel
from .serializers import ImageSerializer
from .utils import get_minio_client, get_minio_bucket_url, get_minio_bucket_name, keep_aspect_image_resize


class ImageUploadView(APIView):
    def post(self, request):
        # リクエストから画像のタイトルとファイルを取り出す
        title = request.data.get('title')
        img_file = request.FILES.get('image')
        if (not title) or (not img_file):
            return Response(
                {'error': 'title and image file are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 画像を読み込んでリサイズし、バッファに書き出す
        try:
            # オリジナルの画像
            original_img = Image.open(img_file)
            original_img_buffer = BytesIO()
            original_img.save(original_img_buffer, format='JPEG')
            original_img_buffer.seek(0)

            # 長辺 1000 ピクセルの表示用画像を作成
            display_img = keep_aspect_image_resize(img_file, 1000)
            display_img_buffer = BytesIO()
            display_img.save(display_img_buffer, format='JPEG')
            display_img_buffer.seek(0)

            # 長辺 300 ピクセルのサムネイル画像を作成
            thumbnail_img = keep_aspect_image_resize(img_file, 300)
            thumbnail_img_buffer = BytesIO()
            thumbnail_img.save(thumbnail_img_buffer, format='JPEG')
            thumbnail_img_buffer.seek(0)
        except Exception as e:
            return Response(
                {'error': 'image processing failed: ' + str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # UUID で名前を決定
        original_img_filename = str(uuid.uuid4()) + ".jpg"
        display_img_filename = str(uuid.uuid4()) + ".jpg"
        thumbnail_img_filename = str(uuid.uuid4()) + ".jpg"

        # MinIO のクライアントを取得してそれぞれの画像を保存
        s3 = get_minio_client()
        bucket = get_minio_bucket_name()
        print(bucket, original_img_filename)
        try:
            s3.upload_fileobj(original_img_buffer, bucket, original_img_filename, ExtraArgs={'ContentType': 'image/jpeg'})
            s3.upload_fileobj(display_img_buffer, bucket, display_img_filename, ExtraArgs={'ContentType': 'image/jpeg'})
            s3.upload_fileobj(thumbnail_img_buffer, bucket, thumbnail_img_filename, ExtraArgs={'ContentType': 'image/jpeg'})
        except Exception as e:
            return Response(
                {'error': 'MinIO upload failed: ' + str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # アクセス URL の構築
        original_url = get_minio_bucket_url() + original_img_filename
        display_url = get_minio_bucket_url() + display_img_filename
        thumbnail_url = get_minio_bucket_url() + thumbnail_img_filename

        # モデルに保存
        uploaded_image = ImageModel.objects.create(
            title=title,
            thumbnail_url=thumbnail_url,
            display_url=display_url,
            original_url=original_url
        )
        serializer = ImageSerializer(uploaded_image)
        return Response(serializer.data, status=status.HTTP_201_CREATED)