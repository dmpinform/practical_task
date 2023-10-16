import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)
channel = connection.channel()

# Direct - отправлять сообщения по routing_key
# Routing_key задается при отправке
# Связь очереди и сообщения задаются в привязке
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

severities = ['info', 'warning', 'error']

# Отправить сообщения с разным routing_key
for severity in severities:
    message = f'severity_{severity}'
    channel.basic_publish(
        exchange='direct_logs', routing_key=severity, body=message
    )
    print(f' [x] Sent {severity}:{message}')

connection.close()
