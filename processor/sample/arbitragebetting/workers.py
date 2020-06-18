import json
from multiprocessing import get_logger

from pythontools.messaging.rabbitmq import Consumer, Producer
from pythontools.actionmanager.manager import ActionManager

class OddsConsumer(Consumer):
    def __init__(self, config, outcome_producer, action_manager):
        """
        Initialize consumer instance.
        """
        super().__init__(OddsConsumer.__name__, config)
        self.logger = get_logger()
        self.load_config(config)
        self.outcome_producer = outcome_producer
        self.action_manager = action_manager

    def load_config(self, config):
        """
        Loads config values from dictionary
        """
        try:
            self.logger.info(f"initializing {OddsConsumer.__name__} with {config}")
        except Exception as error:
            self.logger.error(f"invalid configuration for {OddsConsumer.__name__}")
            self.logger.error(error)
            raise error

    def do_work(self, ch, method, properties, body):
        """
        Get some odds from the odds queue and process them to generate outcomes
        """
        self.logger.info(f"received new message with body => {body}")
        success = self.action_manager.run_workflow(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)


    def send_outcomes(self, outcomes):
        """
        Tells the producer to send a serialized version of the outcomes
        """
        self.logger.info("passing the odds to the producer")
        return self.outcome_producer.send_outcomes(outcomes)

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