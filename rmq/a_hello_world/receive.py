import os
import sys

import pika


def main():
    # Создать подключение
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost')
    )
    # Создать канал
    channel = connection.channel()

    # Создать канал
    channel.queue_declare(queue='hello')

    # Создать обработчик полученных сообщений
    def callback(ch, method, properties, body):
        print(f' [x] Received {body}')

    # Подписать обработчик полученных сообщений на очередь
    # Отключить подтверждение сообщения в ручную auto_ack=True
    # Сообщение удалится из очереди после прочтения
    channel.basic_consume(
        queue='hello', on_message_callback=callback, auto_ack=True
    )

    print(' [*] Waiting for messages. To exit press CTRL+C')
    # Войти в цикл, который слушает очередь и обрабатывает сообщения
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
