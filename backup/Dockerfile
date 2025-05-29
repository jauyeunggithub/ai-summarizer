FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y postgresql-client && \
    pip install boto3 psycopg2-binary && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY backup.py restore.py ./
