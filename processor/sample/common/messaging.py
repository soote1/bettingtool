from multiprocessing import get_logger

import pika

from processor.sample.common.model import Worker

HOST_NAME = "host_name"
QUEUE_NAME = "queue_name"
PREFETCH_COUNT = "prefetch_count"
DURABLE = "durable"
WAIT_TIME = "wait_time"
EXCHANGE = "exchange"
DELIVERY_MODE = "delivery_mode"

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
            self.queue_name = config[QUEUE_NAME]
            self.durable = config[DURABLE]
            self.host_name = config[HOST_NAME]
            self.delivery_mode = config[DELIVERY_MODE]
            self.exchange = config[EXCHANGE]
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

class Consumer(Worker): # TODO: fix this, consumer class shouldn't extend from other package
    def __init__(self, name, config):
        """
        Initialize consumer with given config and name and calls connect_to_broker
        to establish the connection with the message broker.
        """
        self.logger = get_logger()
        self.load_consumer_config(config)
        self.connect_to_broker()
    
    def load_consumer_config(self, config):
        try:
            self.logger.info(f"initializing consumer with {config}")
            self.host_name = config[HOST_NAME]
            self.durable = config[DURABLE]
            self.queue_name = config[QUEUE_NAME]
            self.prefetch_count = config[PREFETCH_COUNT]
            self.wait_time = config[WAIT_TIME]
        except Exception as error:
            self.logger.error(f"invalid configuration for {Consumer.__name__} class")
            self.logger.error(error)
            raise error

    def connect_to_broker(self):
        """
        Establishes the connection with the message broker
        using the consumer configuration.
        """
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host_name))
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue_name, durable=self.durable)
            self.channel.basic_qos(prefetch_count=self.prefetch_count)
            self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.do_work)
        except Exception as error:
            self.logger.error("problems found while trying to connect with rabbitmq")
            self.logger.error(error)
            raise error

    def run(self):
        """
        Main method which starts the message consuming process.
        """
        try:
            self.logger.info("starting consuming")
            self.channel.start_consuming()
        except KeyboardInterrupt as error:
            self.logger.info("closing consumer")
            self.channel.close()

    def do_work(self, ch, method, properties, body):
        """
        Abstract method to be implemented by each specific consumer.
        This is the signature for the pika client's on_message_callback method.
        """
        pass

