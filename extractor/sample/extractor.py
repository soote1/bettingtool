import json
from extractor.sample.model.extractor_config_keys import ExtractorConfigKeys
from extractor.sample.helpers.worker_factory import WorkerFactory
from extractor.sample.helpers.config import Config
from multiprocessing import Process

class Extractor:
    def __init__(self, config_helper):
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
            self.seeders.append(WorkerFactory.create_instance(seeder[0], seeder[1]))

    def load_fetchers(self):
        """
        Prepare all fetchers
        """
        fetcher_classes = self.config_helper.get(ExtractorConfigKeys.fetchers())
        for fetcher in fetcher_classes:
            self.seeders.append(WorkerFactory.create_instance(fetcher[0], fetcher[1]))

    def load_listeners(self):
        """
        Prepare all listeners
        """
        listener_classes = self.config_helper.get(ExtractorConfigKeys.listeners())
        for listener in listener_classes:
            self.seeders.append(WorkerFactory.create_instance(listener[0], listener[1]))

    def load_producers(self):
        """
        Prepare all producers
        """
        producer_classes = self.config_helper.get(ExtractorConfigKeys.producers())
        for producer in producer_classes:
            self.seeders.append(WorkerFactory.create_instance(producer[0], producer[1]))

    def load_consumers(self):
        """
        Prepare all consumers
        """
        consumer_classes = self.config_helper.get(ExtractorConfigKeys.consumers())
        for consumer in consumer_classes:
            self.seeders.append(WorkerFactory.create_instance(consumer[0], consumer[1]))
    
    def run(self):
        """
        Run all process
        """
        worker_instances = self.consumers + self.producers + self.fetchers + self.seeders + self.listeners
        print(worker_instances)
        # create processes
        for worker_instance in worker_instances:
            self.processes.append(Process(target=worker_instance.run))

        # start all processes
        for process in self.processes:
            process.start()