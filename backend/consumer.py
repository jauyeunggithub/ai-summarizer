import time
from helpers.queue import channel, QUEUE_NAME


def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")
    # simulate task
    time.sleep(1)
    print(" [x] Done")


def consume():
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE_NAME,
                          on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    consume()
