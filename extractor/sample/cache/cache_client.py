from walrus import *
import os

from extractor.sample.cache.cache_client_config_keys import CacheClientConfigkeys
from multiprocessing import get_logger

class CacheClient:
    def __init__(self):
        """
        Loads the configuration from the json file and then creates the redis client
        """
        with open(f"{os.path.dirname(__file__)}/config.json") as json_config:
            config = json.load(json_config)

        self.logger = get_logger()
        self.load_client_config(config)
        self.client = Walrus(host=self.host, port=self.port, db=self.db)
    
    def load_client_config(self, config):
        """
        Loads the configuration values from a dictionary object
        """
        self.logger.info(f"Initializing {CacheClient.__name__} with {config}")
        self.host = config[CacheClientConfigkeys.host()]
        self.port = config[CacheClientConfigkeys.port()]
        self.db = config[CacheClientConfigkeys.db()]

    def clean_cache(self):
        """
        Removes all the keys stored in the redis server
        """
        self.client.flushall()