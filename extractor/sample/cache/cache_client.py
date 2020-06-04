from walrus import *
import os

class CacheClient:
    def __init__(self):
        with open(f"{os.path.dirname(__file__)}/config.json") as json_config:
            self.config = json.load(json_config)
        self.client = Walrus(host=self.config["host"], port=self.config["port"], db=self.config["db"])

    def save_key_value(self, key, value):
        self.client.set(key, value)
    
    def get_value(self, key):
        return self.client.get(key)