import sys

import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)
channel = connection.channel()

# Обменник (exchange) - получает сообщения от издателя и помещает их в очереди
# Правила распределения сообщений определяются типом обмена:
# direct, topic, headers, fanout
# Fanout - отправлять сообщения во все очереди
channel.exchange_declare(exchange='logs', exchange_type='fanout')

message = ' '.join(sys.argv[1:]) or 'info: Hello World!'

# С типом обмена fanout, routing_key=''
channel.basic_publish(exchange='logs', routing_key='', body=message)
print(f' [x] Sent {message}')
connection.close()
