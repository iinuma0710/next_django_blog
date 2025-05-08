import os
import boto3
from botocore.client import Config
from PIL import Image


def keep_aspect_image_resize(img_file, long_side):
    img = Image.open(img_file)
    if img.height < img.width:
        resize_w = long_side
        resize_h = round(img.height * resize_w / img.width)
    else:
        resize_h = long_side
        resize_w = round(img.width * resize_h / img.height)
    return img.resize((resize_w, resize_h))


def get_minio_bucket_name():
    return os.getenv('MINIO_BUCKET_NAME')


def get_minio_bucket_url():
    endpoint = os.getenv('MINIO_ENDPOINT')
    bucket = os.getenv('MINIO_BUCKET_NAME')
    use_ssl = os.getenv('MINIO_USE_SSL', 'False').lower() == 'true'
    return f"http{'s' if use_ssl else ''}://{endpoint}/{bucket}/"


def get_minio_client():
    endpoint = os.getenv('MINIO_ENDPOINT')
    access_key = os.getenv('MINIO_ACCESS_KEY')
    secret_key = os.getenv('MINIO_SECRET_KEY')
    use_ssl = os.getenv('MINIO_USE_SSL', 'False').lower() == 'true'

    return boto3.client(
        's3',
        endpoint_url=f"http{'s' if use_ssl else ''}://{endpoint}",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )