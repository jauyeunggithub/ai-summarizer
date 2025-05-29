import os
import subprocess
import boto3


def restore_database(s3_key):
    s3_bucket = os.environ['S3_BUCKET_NAME']
    aws_region = os.environ['AWS_REGION']
    db_user = os.environ.get('POSTGRES_USER', 'postgres')
    db_password = os.environ.get('POSTGRES_PASSWORD', 'postgres')
    db_host = os.environ.get('DB_HOST', 'db')
    db_name = os.environ.get('POSTGRES_DB', 'postgres')

    restore_file = f"/tmp/{os.path.basename(s3_key)}"

    # Download dump from S3
    s3_client = boto3.client('s3', region_name=aws_region)
    print(f"Downloading backup from s3://{s3_bucket}/{s3_key} ...")
    s3_client.download_file(s3_bucket, s3_key, restore_file)
    print("Download complete.")

    # Set password for pg_restore
    os.environ['PGPASSWORD'] = db_password

    # Drop existing DB and recreate (optional, use with caution)
    drop_cmd = ['psql', '-h', db_host, '-U', db_user,
                '-c', f'DROP DATABASE IF EXISTS {db_name};']
    create_cmd = ['psql', '-h', db_host, '-U',
                  db_user, '-c', f'CREATE DATABASE {db_name};']

    subprocess.run(drop_cmd, check=True)
    subprocess.run(create_cmd, check=True)

    # Restore DB from dump
    restore_cmd = [
        'pg_restore',
        '-h', db_host,
        '-U', db_user,
        '-d', db_name,
        '-c',
        restore_file
    ]

    print(f"Restoring database from {restore_file} ...")
    subprocess.run(restore_cmd, check=True)
    print("Restore complete.")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python restore.py <s3_key>")
        exit(1)
    restore_database(sys.argv[1])
