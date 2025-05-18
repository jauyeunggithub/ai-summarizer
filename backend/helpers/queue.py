import pika


QUEUE_NAME = 'task_queue'

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq')
)
channel = connection.channel()
