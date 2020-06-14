import os
import json
from multiprocessing import get_logger

from walrus import Walrus, Model

class BaseModel(Model):
    pass

class CacheClient:
    HOST = "host"
    PORT = "port"
    DB = "db"
    def __init__(self, config):
        """
        Initialize cache client instance
        """
        self.client = Walrus(
            host=config[CacheClient.HOST], 
            port=config[CacheClient.PORT], 
            db=config[CacheClient.DB])

    def clean_cache(self):
        """
        Removes all the keys stored in the redis server
        """
        self.client.flushall()