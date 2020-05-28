import json

class Config:
    def __init__(self, config_str):
        self.config = self.parse_config(config_str)

    def parse_config(self, config_str):
        return json.loads(config_str)
    
    def get(self, key):
        return self.config[key]