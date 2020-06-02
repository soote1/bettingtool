import json
import logging
import time
from multiprocessing import Event, Process, get_logger, log_to_stderr

from extractor.sample.config.extractor_config_keys import ExtractorConfigKeys
from extractor.sample.config.config import Config
from extractor.sample.workers.worker_factory import WorkerFactory

class Extractor:
    def __init__(self, config_helper):
        """
        Initialize logger and attributes
        """
        log_to_stderr()
        self.logger = get_logger()
        self.logger.setLevel(logging.INFO)
        self.consumers = []
        self.producers = []
        self.seeders = []
        self.fetchers = []
        self.listeners = []
        self.processes = []
        self.config_helper = config_helper
        self.load_config()
    
    def load_config(self):
        """
        Parse config string into a dictionary and initialize the objects
        """
        self.logger.info(f"Loading extractor config {self.config_helper.config}")
        self.load_producers()
        self.load_consumers()
        self.load_seeders()
        self.load_fetchers()

    def load_seeders(self):
        """
        Prepare all seeders
        """
        seeder_classes = self.config_helper.get(ExtractorConfigKeys.seeders())
        for seeder in seeder_classes:
            self.seeders.append(WorkerFactory.create_instance(seeder[0], seeder[1], seeder[2]))

    def load_fetchers(self):
        """
        Prepare all fetchers
        """
        fetcher_classes = self.config_helper.get(ExtractorConfigKeys.fetchers())
        for fetcher in fetcher_classes:
            self.seeders.append(WorkerFactory.create_instance(fetcher[0], fetcher[1], fetcher[2]))

    def load_listeners(self):
        """
        Prepare all listeners
        """
        listener_classes = self.config_helper.get(ExtractorConfigKeys.listeners())
        for listener in listener_classes:
            self.seeders.append(WorkerFactory.create_instance(listener[0], listener[1], listener[2]))

    def load_producers(self):
        """
        Prepare all producers
        """
        producer_classes = self.config_helper.get(ExtractorConfigKeys.producers())
        for producer in producer_classes:
            self.seeders.append(WorkerFactory.create_instance(producer[0], producer[1], producer[2]))

    def load_consumers(self):
        """
        Prepare all consumers
        """
        consumer_classes = self.config_helper.get(ExtractorConfigKeys.consumers())
        for consumer in consumer_classes:
            self.seeders.append(WorkerFactory.create_instance(consumer[0], consumer[1], consumer[2]))
    
    def run(self):
        """
        Run all process
        """
        keyboard_interrupt_event = Event()
        worker_instances = self.consumers + self.producers + self.fetchers + self.seeders + self.listeners
        print(worker_instances)
        # create processes
        for worker_instance in worker_instances:
            self.processes.append(Process(target=worker_instance.run, args=(keyboard_interrupt_event,)))

        # start all processes
        for process in self.processes:
            process.start()

        while True:
            try:
                time.sleep(self.config_helper.get(ExtractorConfigKeys.wait_time()))
            except KeyboardInterrupt as error:
                self.logger.info("sending shutdown signal to child processes")
                keyboard_interrupt_event.set()
                break
        
        for process in self.processes:
            process.join()

