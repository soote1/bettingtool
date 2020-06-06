import pika
from multiprocessing import get_logger

from extractor.sample.messaging.messaging_config_keys import MessagingConfigKeys

class Producer:
    def __init__(self, config):
        """
        Initialize producer with given config.
        """
        self.logger = get_logger()
        self.connection = None
        self.channel = None
        self.load_config(config)

    def load_config(self, config):
        try:
            self.logger.info(f"loading {Producer.__name__} with {config}")
            self.queue_name = config[MessagingConfigKeys.queue_name()]
            self.durable = config[MessagingConfigKeys.durable()]
            self.host_name = config[MessagingConfigKeys.host_name()]
            self.delivery_mode = config[MessagingConfigKeys.delivery_mode()]
            self.exchange = config[MessagingConfigKeys.exchange()]
        except Exception as error:
            self.logger.error(f"invalid configuration for {Producer.__name__}")
            self.logger.error(error)
            raise error

    def produce(self, message):
        """
        Sends a new message to a queue.
        Calls connect_to_broker() if the current connection hasn't been established.
        """
        self.logger.info(f"sending {message} to {self.queue_name}")
        if self.connection == None:
            self.connect_to_broker()
        
        try:
            self.channel.basic_publish(
                exchange=self.exchange,
                routing_key=self.queue_name,
                body=message,
                properties=pika.BasicProperties(delivery_mode=self.delivery_mode,)
            )
        except Exception as error:
            self.logger.error(f"problems found while trying to send {message} to {self.queue_name}")
            self.logger.error(error)
            return False
        
        return True

    def connect_to_broker(self):
        """
        Establishes the connection with the message broker and creates the queue if it doesn't exists.
        """
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host_name))
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue_name, durable=self.durable)
        except Exception as error:
            self.logger.error("problems found while trying to connect with rabbitmq server")
            self.logger.error(error)
            raise error