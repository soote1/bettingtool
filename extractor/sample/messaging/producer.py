import pika
from extractor.sample.messaging.messaging_config_keys import MessagingConfigKeys

class Producer:
    def __init__(self, config):
        """
        Initialize producer with given config.
        """
        self.connection = None
        self.channel = None
        self.load_config(config)

    def load_config(self, config):
        self.queue_name = config[MessagingConfigKeys.queue_name()]
        self.durable = config[MessagingConfigKeys.durable()]
        self.host_name = config[MessagingConfigKeys.host_name()]
        self.delivery_mode = config[MessagingConfigKeys.delivery_mode()]
        self.exchange = config[MessagingConfigKeys.exchange()]

    def produce(self, message):
        """
        Sends a new message to a queue.
        Calls connect_to_broker() if the current connection hasn't been established.
        """
        self.logger.info(f"sending {message} to {self.queue_name}")
        if self.connection == None:
            self.connect_to_broker()
        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=self.queue_name,
            body=message,
            properties=pika.BasicProperties(delivery_mode=self.delivery_mode,)
        )

    def connect_to_broker(self):
        """
        Establishes the connection with the message broker and creates the queue if it doesn't exists.
        """
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host_name))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name, durable=self.durable)