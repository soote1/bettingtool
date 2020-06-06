from walrus import *
import os

from extractor.sample.cache.cache_client_config_keys import CacheClientConfigkeys
from multiprocessing import get_logger

class CacheClient:
    def __init__(self):
        """
        Loads the configuration from the json file and then creates the redis client
        """
        self.logger = get_logger()
        config = self.get_config_from_file("/config.json")
        self.load_client_config(config)
        self.client = Walrus(host=self.host, port=self.port, db=self.db)
    
    def get_config_from_file(self, path):
        full_path = f"{os.path.dirname(__file__)}{path}"
        self.logger.info(f"loading config from {full_path}")
        try:
            with open(full_path) as json_config:
                config = json.load(json_config)
        except Exception as error:
            self.logger.error(f"problems found while loading config json file for {CacheClient.__name__}")
            self.logger.error(error)
            raise error

        return config
    
    def load_client_config(self, config):
        """
        Loads the configuration values from a dictionary object
        """
        try:
            self.logger.info(f"Initializing {CacheClient.__name__} with {config}")
            self.host = config[CacheClientConfigkeys.host()]
            self.port = config[CacheClientConfigkeys.port()]
            self.db = config[CacheClientConfigkeys.db()]
        except Exception as error:
            self.logger.error(f"invalid configuration for {CacheClient.__name__} class")
            self.logger.error(error)
            raise error

    def clean_cache(self):
        """
        Removes all the keys stored in the redis server
        """
        self.client.flushall()