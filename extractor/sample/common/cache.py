import os
import json
from multiprocessing import get_logger

from walrus import Walrus, Model

full_path = f"{os.path.dirname(__file__)}/cache_config.json"
with open(full_path) as json_config:
    config = json.load(json_config)
database = Walrus(host=config["host"], port=config["port"], db=config["db"])

class BaseModel(Model):
    __database__ = database

class CacheClient:
    def __init__(self):
        """
        Initialize cache client instance
        """
        self.client = database

    def clean_cache(self):
        """
        Removes all the keys stored in the redis server
        """
        self.client.flushall()