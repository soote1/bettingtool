import pika
from extractor.sample.workers.worker import Worker
from multiprocessing import get_logger

class Consumer(Worker):
    def __init__(self, name, config):
        super().__init__(name, config["wait_time"])
        self.config = config
        self.logger = get_logger()
        self.logger.info(f"initializing {name} with {config}")
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.config["host_name"]))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.config["queue_name"], durable=self.config["durable"])
        self.channel.basic_qos(prefetch_count=self.config["prefetch_count"])
        self.channel.basic_consume(queue=self.config["queue_name"], on_message_callback=self.receive)

    def run(self, shutdown_event):
            try:
                self.logger.info("starting consuming")
                self.channel.start_consuming()

            except KeyboardInterrupt as error:
                self.channel.close()

    def receive(self, ch, method, properties, body):
        pass