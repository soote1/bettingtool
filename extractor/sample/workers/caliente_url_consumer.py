from extractor.sample.messaging.consumer import Consumer
from extractor.sample.workers.caliente_fetcher import CalienteFetcher
from extractor.sample.workers.caliente_odds_producer import CalienteOddsProducer
from multiprocessing import get_logger
import json

class CalienteUrlConsumer(Consumer):
    def __init__(self, config):
        super().__init__(CalienteUrlConsumer.__name__, config)
        self.logger = get_logger()
        self.logger.info(f"initializing {CalienteUrlConsumer.__name__} with {self.config}")
        self.odds_fetcher = CalienteFetcher()
        self.odds_producer = CalienteOddsProducer(self.config["producer_config"])

    def receive(self, ch, method, properties, body):
        self.logger.info(f"received new message with body => {body}")
        odds = self.odds_fetcher.fetch(body.decode("utf-8"))
        if not odds == None:
            self.send_odds(odds)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def send_odds(self, odds):
        serialized_product = json.dumps(odds.__dict__)
        self.odds_producer.send_odds(serialized_product)