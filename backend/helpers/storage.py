import boto3
from botocore.exceptions import BotoCoreError, ClientError
import os

aws_access_key = os.getenv('AWS_ACCESS_KEY')
with open("/run/secrets/aws_secret_access_key.txt", "r") as secret_file:
    aws_secret_access_key = secret_file.read().strip()

s3 = boto3.client(
    's3',
    region_name='us-east-1',
    aws_access_key=aws_access_key,
    aws_secret_key=aws_secret_access_key
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
