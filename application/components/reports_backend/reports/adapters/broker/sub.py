class Sub:

    def __init__(self, connection, channel):
        self.connection = connection
        self.channel = channel
        self.run_task = None

    def callback(self, ch, method, properties, body):
        self.run_task(body)
        print(f' [x] Done {body}')
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start(self, queue: str, run_task):
        self.run_task = run_task
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue=queue, on_message_callback=self.callback
        )
        self.channel.start_consuming()
