import pika


class Pub:

    def __init__(self, connection, channel):
        self.connection = connection
        self.channel = channel

    def send_message(self, message: str, routing_key: str):
        self.channel.basic_publish(
            exchange='',
            routing_key=routing_key,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
            )
        )
        print(f' [x] Sent {message}')

    def set_tmp_user_channel(self, channel_name):
        self.channel.queue_declare(
            queue=channel_name,
            durable=True,
            auto_delete=True,
        )
