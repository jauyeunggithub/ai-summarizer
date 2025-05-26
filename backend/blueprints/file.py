from flask import Blueprint, Response, request, abort
import requests
from helpers.storage import extract_bucket_and_key_from_url, is_s3_url
import os
from botocore.exceptions import ClientError
import boto3
from botocore.config import Config


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

file_blueprint = Blueprint('file', __name__)


@file_blueprint.route('/fetch_file', methods=['GET'])
def fetch_file_view():
    url = request.args.get('url')
    if not url:
        return abort(400, "Missing 'url' parameter")

    if is_s3_url(url):
        bucket, key = extract_bucket_and_key_from_url(url)
        if not bucket or not key:
            return abort(400, "Invalid S3 URL")

        try:
            s3_obj = s3.get_object(Bucket=bucket, Key=key)
            return Response(
                s3_obj['Body'].read(),
                mimetype=s3_obj.get('ContentType', 'application/octet-stream'),
                headers={
                    "Content-Disposition": f"inline; filename={key.split('/')[-1]}"}
            )
        except ClientError as e:
            return abort(404, f"S3 object not found or inaccessible: {e}")

    else:
        try:
            resp = requests.get(url, stream=True)
            resp.raise_for_status()
            headers = {
                "Content-Disposition": f"inline; filename={url.split('/')[-1]}",
                "Content-Type": resp.headers.get('Content-Type', 'application/octet-stream')
            }
            return Response(resp.iter_content(chunk_size=8192), headers=headers)
        except requests.RequestException as e:
            return abort(404, f"Failed to fetch file from URL: {e}")
