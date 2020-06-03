import pika

class Producer:
    def __init__(self, config):
        self.config = config
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.config["host_name"]))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.config["queue_name"], durable=self.config["durable"])

    def produce(self, message):
        self.channel.basic_publish(
            exchange=self.config["exchange"],
            routing_key=self.config["queue_name"],
            body=message,
            properties=pika.BasicProperties(delivery_mode=self.config["delivery_mode"],)
        )

    def __del__(self):
        self.connection.close()