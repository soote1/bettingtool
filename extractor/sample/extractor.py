import json
from extractor.sample.model.extractor_config_keys import ExtractorConfigKeys

class Extractor:
    def __init__(self, config_str):
        self.consumers = []
        self.producers = []
        self.seeders = []
        self.fetchers = []
        self.load_listeners = []
        self.load_config(config_str)
    
    def load_cofig(self, config_str):
        """
        Parse config string into a dictionary and initialize the objects
        """
        self.config = json.loads(config_str)
        self.load_producers(config[ExtractorConfigKeys.producers()])
        self.load_consumers(config[ExtractorConfigKeys.consumers()])
        self.load_seeders(config[ExtractorConfigKeys.seeders()])
        self.load_fetchers(config[ExtractorConfigKeys.fetchers()])

    def load_seeders(self, seeder_classes_str):
        """
        Prepare all seeders
        """
        seeder_classes = config[ExtractorConfigKeys.seeders()].split(',')

    def load_fetchers(self, fetcher_classes_str):
        """
        Prepare all fetchers
        """
        fetcher_classes = config[ExtractorConfigKeys.fetchers()].split(',')

    def load_listeners(self, listener_classes_str):
        """
        Prepare all listeners
        """
        listener_classes = config[ExtractorConfigKeys.listeners()].split(',')
        

    def load_producers(self, producer_classes_str):
        """
        Prepare all producers
        """
        producer_classes = config[ExtractorConfigKeys.producers()].split(',')

    def load_consumers(self, consumer_classes_str):
        """
        Prepare all consumers
        """
        consumer_classes = config[ExtractorConfigKeys.consumers()].split(',')
    
    def run(self):
        """
        Run all process
        """
        pass