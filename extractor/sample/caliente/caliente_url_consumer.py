from extractor.sample.messaging.consumer import Consumer
from extractor.sample.caliente.caliente_fetcher import CalienteFetcher
from extractor.sample.caliente.caliente_odds_producer import CalienteOddsProducer
from extractor.sample.caliente.caliente_url_consumer_config_keys import CalienteUrlConsumerConfigKeys
from multiprocessing import get_logger
import json

class CalienteUrlConsumer(Consumer):
    def __init__(self, config):
        """
        Initialize consumer instance.
        """
        self.logger = get_logger()
        super().__init__(CalienteUrlConsumer.__name__, config)
        self.load_config(config)
        self.odds_fetcher = CalienteFetcher(self.fetcher_config)
        self.odds_producer = CalienteOddsProducer(self.producer_config)

    def load_config(self, config):
        self.logger.info(f"initializing {CalienteUrlConsumer.__name__} with {config}")
        self.producer_config = config[CalienteUrlConsumerConfigKeys.producer_config()]
        self.fetcher_config = config[CalienteUrlConsumerConfigKeys.fetcher_config()]
        self.decode_format = config[CalienteUrlConsumerConfigKeys.decode_format()]

    def receive(self, ch, method, properties, body):
        """
        This method is called when a message is received in the configured queue.
        It tells the fetcher to process the url and waits for the result. If the
        result isn't None, then it calls the send_odds method and passes the fetcher's
        result as argument.
        """
        self.logger.info(f"received new message with body => {body}")
        odds = self.odds_fetcher.fetch(body.decode(self.decode_format))
        if not odds == None:
            self.send_odds(odds)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def send_odds(self, odds):
        """
        Tells the producer to send a serialized version of the odds to the configured queue.
        """
        serialized_product = json.dumps(odds.__dict__)
        self.odds_producer.send_odds(serialized_product)