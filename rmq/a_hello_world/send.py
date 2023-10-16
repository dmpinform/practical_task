import pika

# Создать подключение
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)

# Создать канал
channel = connection.channel()

# Создать очередь hello - команда идемпотентна.
# Можно запускать несколько раз, при этом создается одна очередь.
channel.queue_declare(queue='hello')

# Отправить сообщение в очередь hello
# Для распределения сообщений всегда нужен exchange
# Если не указан, то создается по умолчанию
# Правило распределения сообщения routing_key
# В данном случае routing_key это имя очереди
channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()
