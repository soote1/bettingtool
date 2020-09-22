import json
from multiprocessing import get_logger

from pythontools.messaging.rabbitmq import Producer

class OutcomeProducer(Producer):
    def __init__(self, config):
        """
        Initialize outcome producer.
        """
        super().__init__(config)
        self.logger = get_logger()
        self.logger.info(f"initializing {OutcomeProducer.__name__} with {config}")

    def send_outcomes(self, odds):
        """
        This method serializes the outcomes and calls produce method, 
        which is inherited from base Producer class,
        and passes the serialized odds as argument.
        """
        self.logger.info(f"serializing {odds} to json format")
        serialized_product = json.dumps(odds.__dict__, default=str)
        return self.produce(serialized_product)