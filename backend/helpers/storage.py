import boto3
from botocore.exceptions import BotoCoreError, ClientError
from botocore.config import Config
import os
from urllib.parse import urlparse, unquote


aws_access_key = os.getenv('AWS_ACCESS_KEY')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_REGION')

s3 = boto3.client(
    's3',
    region_name=aws_region,
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_access_key,
    config=Config(signature_version='s3v4')
)


def upload_file_to_s3(file_path, bucket_name, object_name=None):
    import os
    if object_name is None:
        object_name = os.path.basename(file_path)

    try:
        s3.upload_file(file_path, bucket_name, object_name)
        url = f"https://{bucket_name}.s3.amazonaws.com/{object_name}"
        return {"success": True, "url": url}
    except (BotoCoreError, ClientError) as e:
        return {"success": False, "error": str(e)}


def delete_file_from_s3(bucket_name, object_name):
    try:
        s3.delete_object(Bucket=bucket_name, Key=object_name)
        return {"success": True, "message": f"{object_name} deleted from {bucket_name}"}
    except (BotoCoreError, ClientError) as e:
        return {"success": False, "error": str(e)}


def extract_bucket_and_key_from_url(s3_url):
    parsed = urlparse(unquote(s3_url))
    host_parts = parsed.netloc.split('.')

    if 's3' in host_parts:
        bucket_name = host_parts[0]
        key = parsed.path.lstrip('/')
    else:
        path_parts = parsed.path.lstrip('/').split('/', 1)
        if len(path_parts) < 2:
            return None, None
        bucket_name, key = path_parts

    return bucket_name, key


def is_s3_url(url):
    parsed = urlparse(url)
    return 's3' in parsed.netloc or parsed.netloc.endswith('amazonaws.com')


def delete_s3_file_from_url(s3_url):
    parsed_url = urlparse(s3_url)
    hostname = parsed_url.netloc
    path = parsed_url.path.lstrip('/')
    bucket = None
    key = None

    if hostname.endswith("amazonaws.com") and '.s3.' in hostname:
        bucket = hostname.split('.')[0]
        key = path

    elif hostname.startswith("s3.") and hostname.endswith("amazonaws.com"):
        parts = path.split('/', 1)
        if len(parts) == 2:
            bucket, key = parts
        else:
            raise ValueError("URL does not contain bucket and key properly.")

    else:
        raise ValueError("URL format not recognized as S3 URL.")

    try:
        s3.delete_object(Bucket=bucket, Key=key)
        print(f"Deleted {key} from bucket {bucket}")
    except Exception as e:
        print(f"Error deleting object: {e}")
