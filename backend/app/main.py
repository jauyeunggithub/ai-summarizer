from flask import Flask, jsonify, request
import threading
import pika
import os
import psycopg2

app = Flask(__name__)

# Read DB password from Docker secret file


def get_db_password():
    try:
        with open("/run/secrets/db_password", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        # Fallback to environment variable if secret file is not found
        return os.getenv("DB_PASSWORD", "postgres")


# Construct DATABASE_URL with the secret password
DB_PASSWORD = get_db_password()
DATABASE_URL = f"postgresql://postgres:{DB_PASSWORD}@db:6000/postgres"


def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

# Basic route


@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello from Flask API!"})

# RabbitMQ listener


def rabbitmq_listener():
    rabbitmq_host = os.getenv("RABBITMQ_HOST", "rabbitmq")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()
    channel.queue_declare(queue='test_queue', durable=True)

    def callback(ch, method, properties, body):
        print("Received:", body.decode())
        try:
            conn = get_db_connection()
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO messages (content) VALUES (%s)", (body.decode(),))
                conn.commit()
            conn.close()
        except Exception as e:
            print("Database error:", e)

    channel.basic_consume(queue='test_queue',
                          on_message_callback=callback, auto_ack=True)
    print('Waiting for RabbitMQ messages. To exit press CTRL+C')
    channel.start_consuming()

# Run background listener thread


def start_listener():
    listener_thread = threading.Thread(target=rabbitmq_listener, daemon=True)
    listener_thread.start()


if __name__ == "__main__":
    start_listener()
    app.run(host='0.0.0.0', port=5000)
