import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)
channel = connection.channel()

# Задать прямой тип обменника
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')


# Задать соотвествие очередей и ключей
def bind(queue_name, routing_keys):
    channel.queue_declare(queue=queue_name, exclusive=False)
    for severity in routing_keys:
        channel.queue_bind(
            exchange='direct_logs', queue=queue_name, routing_key=severity
        )


bind('info_warning', ['info', 'warning'])
bind('error', ['error'])

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(f' [x] {method.routing_key}:{body}')


channel.basic_consume(
    queue='info_warning', on_message_callback=callback, auto_ack=True
)
channel.basic_consume(
    queue='error', on_message_callback=callback, auto_ack=True
)

channel.start_consuming()
