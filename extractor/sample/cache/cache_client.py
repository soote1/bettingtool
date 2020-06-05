from walrus import *
import os

from extractor.sample.cache.cache_client_config_keys import CacheClientConfigkeys
from multiprocessing import get_logger

class CacheClient:
    def __init__(self):
        with open(f"{os.path.dirname(__file__)}/config.json") as json_config:
            config = json.load(json_config)

        self.logger = get_logger()
        self.load_client_config(config)
        self.client = Walrus(host=self.host, port=self.port, db=self.db)
    
    def load_client_config(self, config):
        self.logger.info(f"Initializing {CacheClient.__name__} with {config}")
        self.host = config[CacheClientConfigkeys.host()]
        self.port = config[CacheClientConfigkeys.port()]
        self.db = config[CacheClientConfigkeys.db()]

    def save_key_value(self, key, value):
        self.client.set(key, value)
    
    def get_value(self, key):
        return self.client.get(key)