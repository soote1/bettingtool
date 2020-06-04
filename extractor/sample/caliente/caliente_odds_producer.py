from multiprocessing import get_logger
from extractor.sample.messaging.producer import Producer

class CalienteOddsProducer(Producer):
    def __init__(self, config):
        super().__init__(config)
        self.logger = get_logger()
        self.logger.info(f"initializing {CalienteOddsProducer.__name__} with {self.config}")

    def send_odds(self, serialized_odds):
        self.logger.info(f"seding {serialized_odds} to {self.config['queue_name']}")
        self.produce(serialized_odds)