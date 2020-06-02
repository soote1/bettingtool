from walrus import *

class CacheClient:
    def __init__(self):
        self.client = Walrus(host="localhost", port=6379, db=0)

    def save_key_value(self, key, value):
        self.client.set(key, value)
    
    def get_value(self, key):
        return self.client.get(key)