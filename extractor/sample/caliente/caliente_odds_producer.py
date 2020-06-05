from multiprocessing import get_logger
from extractor.sample.messaging.producer import Producer

class CalienteOddsProducer(Producer):
    def __init__(self, config):
        """
        Initialize odds producer.
        """
        super().__init__(config)
        self.logger = get_logger()
        self.logger.info(f"initializing {CalienteOddsProducer.__name__} with {config}")

    def send_odds(self, serialized_odds):
        """
        This method calls produce method, which is inherited from Producer class,
        and passes the serialized odds as argument.
        """
        self.produce(serialized_odds)