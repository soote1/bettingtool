import json
import logging
import time
from multiprocessing import Event, Process, get_logger, log_to_stderr

from extractor.sample.config.config_keys import ConfigKeys
from extractor.sample.config.config_helper import ConfigHelper
from extractor.sample.workers.worker_factory import WorkerFactory

class Extractor:
    def __init__(self, config_helper):
        """
        Initialize extractor instance.
        """
        log_to_stderr()
        self.logger = get_logger()
        self.logger.setLevel(logging.INFO)
        self.consumers = []
        self.seeders = []
        self.processes = []
        self.config_helper = config_helper
        self.load_config()
    
    def load_config(self):
        """
        Creates workers instances.
        """
        self.logger.info(f"Loading extractor config {self.config_helper.config}")
        self.load_consumers()
        self.load_seeders()

    def load_seeders(self):
        """
        Creates seeder instances.
        """
        seeder_classes = self.config_helper.get(ConfigKeys.seeders())
        self.seeders = [WorkerFactory.create_instance(seeder[ConfigKeys.worker_module()], seeder[ConfigKeys.worker_class()], seeder[ConfigKeys.worker_config()]) for seeder in seeder_classes]

    def load_consumers(self):
        """
        Creates consumer instances.
        """
        consumer_classes = self.config_helper.get(ConfigKeys.consumers())
        self.consumers = [WorkerFactory.create_instance(consumer[ConfigKeys.worker_module()], consumer[ConfigKeys.worker_class()], consumer[ConfigKeys.worker_config()]) for consumer in consumer_classes]
    
    def run(self):
        """
        Runs all process and stop them when keyboard interrupt signal is received.
        """
        keyboard_interrupt_event = Event()
        worker_instances = self.consumers + self.seeders
        print(worker_instances)
        # create processes
        for worker_instance in worker_instances:
            self.processes.append(Process(target=worker_instance.run, args=(keyboard_interrupt_event,)))

        # start all processes
        for process in self.processes:
            process.start()

        while True:
            try:
                time.sleep(self.config_helper.get(ConfigKeys.wait_time()))
            except KeyboardInterrupt as error:
                self.logger.info("sending shutdown signal to child processes")
                keyboard_interrupt_event.set()
                break
        
        for process in self.processes:
            process.join()

