import time

import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(f' [x] Received {body.decode()}')
    # Запустить выполнение задачи
    run_task(body)
    print(' [x] Done')
    # Ручное подтверждение сообщения
    # Важно не забывать подтверждать если auto_ack=False
    ch.basic_ack(delivery_tag=method.delivery_tag)


def run_task(message: bytes):
    # Имитация разной скорости выполнения задачи
    time.sleep(message.count(b'.'))


# Круговая диспетчеризация - обработчики последовательно принимают сообщения
# Честная диспетчеризация - отправлять не более 1 сообщения пока не обработано
# и не подтверждено предыдущее
channel.basic_qos(prefetch_count=1)

channel.basic_consume(queue='task_queue', on_message_callback=callback)

channel.start_consuming()
