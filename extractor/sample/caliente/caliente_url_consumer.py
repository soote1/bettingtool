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
        """
        Loads config values from dictionary
        """
        try:
            self.logger.info(f"initializing {CalienteUrlConsumer.__name__} with {config}")
            self.producer_config = config[CalienteUrlConsumerConfigKeys.producer_config()]
            self.fetcher_config = config[CalienteUrlConsumerConfigKeys.fetcher_config()]
            self.decode_format = config[CalienteUrlConsumerConfigKeys.decode_format()]
        except Exception as error:
            self.logger.error(f"invalid configuration for {CalienteUrlConsumer.__name__}")
            self.logger.error(error)
            raise error

    def receive(self, ch, method, properties, body):
        """
        This method is called when a message is received in the configured queue.
        It tells the fetcher to process the url and waits for the result. If the
        result isn't None, then it calls the send_odds method and passes the fetcher's
        result as argument.
        """
        self.logger.info(f"received new message with body => {body}")
        odds = self.get_odds_from_fetcher(body.decode(self.decode_format))
        if not odds == None:
            odds_sent = self.send_odds(odds)
            if odds_sent:
                self.logger.info("message sent... removing from queue")
                ch.basic_ack(delivery_tag=method.delivery_tag)
            else:
                self.logger.info("the message couldn't be delivered to the queue... keeping in it for next attempt")

    def get_odds_from_fetcher(self, url):
        """
        Tells the fetcher to retrieve the odds for a given url
        """
        self.logger.info("passing url to fetcher and waiting for the odds")
        return self.odds_fetcher.fetch(url)


    def send_odds(self, odds):
        """
        Tells the producer to send a serialized version of the odds to the configured queue.
        """
        self.logger.info("passing the odds to the producer")
        return self.odds_producer.send_odds(odds)