import pika

class Producer:
    def __init__(self, config):
        self.config = config
        self.connection = None
        self.channel = None

    def produce(self, message):
        if self.connection == None:
            self.connect_to_broker()
        self.channel.basic_publish(
            exchange=self.config["exchange"],
            routing_key=self.config["queue_name"],
            body=message,
            properties=pika.BasicProperties(delivery_mode=self.config["delivery_mode"],)
        )

    def connect_to_broker(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.config["host_name"]))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.config["queue_name"], durable=self.config["durable"])