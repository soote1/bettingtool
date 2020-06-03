from extractor.sample.messaging.consumer import Consumer
from multiprocessing import get_logger

class CalienteUrlConsumer(Consumer):
    def __init__(self, config):
        super().__init__(CalienteUrlConsumer.__name__, config)
        self.logger = get_logger()
        self.logger.info(f"initializing {CalienteUrlConsumer.__name__} with {self.config}")

    def receive(self, ch, method, properties, body):
        self.logger.info(f"received new message with body => {body}")
        ch.basic_ack(delivery_tag=method.delivery_tag)