import json
from multiprocessing import get_logger

from pythontools.messaging.rabbitmq import Consumer, Producer
from pythontools.actionmanager.manager import ActionManager

class OddsConsumer(Consumer):
    def __init__(self, config, action_manager):
        """
        Initialize consumer instance.
        """
        super().__init__(OddsConsumer.__name__, config)
        self.logger = get_logger()
        self.load_config(config)
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
        success = self.action_manager.run_workflow(body.decode())
        ch.basic_ack(delivery_tag=method.delivery_tag)