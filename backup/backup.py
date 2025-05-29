import os
import subprocess
import boto3
from datetime import datetime


def backup_database():
    s3_bucket = os.environ['S3_BUCKET_NAME']
    aws_region = os.environ['AWS_REGION']
    db_user = os.environ.get('POSTGRES_USER', 'postgres')
    db_password = os.environ.get('POSTGRES_PASSWORD', 'postgres')
    db_host = os.environ.get('DB_HOST', 'db')
    db_name = os.environ.get('POSTGRES_DB', 'postgres')

    backup_file = f"/tmp/backup_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.dump"

    # Set password for pg_dump
    os.environ['PGPASSWORD'] = db_password

    # Run pg_dump
    dump_command = [
        'pg_dump',
        '-h', db_host,
        '-U', db_user,
        '-F', 'c',  # custom format
        '-f', backup_file,
        db_name
    ]

    print("Starting database backup...")
    subprocess.run(dump_command, check=True)
    print(f"Database dumped to {backup_file}")

    # Upload to S3
    s3_client = boto3.client('s3', region_name=aws_region)
    s3_key = f"backups/{os.path.basename(backup_file)}"

    print(f"Uploading backup to s3://{s3_bucket}/{s3_key} ...")
    s3_client.upload_file(backup_file, s3_bucket, s3_key)
    print("Upload complete.")


if __name__ == "__main__":
    backup_database()
