from multiprocessing import get_logger
from extractor.sample.messaging.producer import Producer

import json

class CalienteOddsProducer(Producer):
    def __init__(self, config):
        """
        Initialize odds producer.
        """
        super().__init__(config)
        self.logger = get_logger()
        self.logger.info(f"initializing {CalienteOddsProducer.__name__} with {config}")

    def send_odds(self, odds):
        """
        This method serializes the odds and calls produce method, 
        which is inherited from base Producer class,
        and passes the serialized odds as argument.
        """
        self.logger.info(f"serializing {odds} to json format")
        serialized_product = json.dumps(odds.__dict__)
        return self.produce(serialized_product)