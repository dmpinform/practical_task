import pika


def send_message(message: str):
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        )
    )
    print(f' [x] Sent {message}')


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)
channel = connection.channel()

# Настроить сохранения очереди и сообщений после перезапуска брокера
# Для очереди durable=True
# Для сообщения delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
# Атрибуты очереди нельзя переопределить, нужно создавать новую очередь
channel.queue_declare(queue='task_queue', durable=True)

# Быстрая обработка
send_message('.')

# Медленная обработка
send_message('...')
connection.close()
