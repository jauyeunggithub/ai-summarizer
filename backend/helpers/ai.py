from helpers.queue import channel, QUEUE_NAME
import pika


def generate_ai_summary(message):
    channel.basic_publish(
        exchange='',
        routing_key=QUEUE_NAME,
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,
        )
    )
