import json

class ConfigHelper:
    def __init__(self, config_str):
        """
        Initialize config helper
        """
        self.config = self.parse_config(config_str)

    def parse_config(self, config_str):
        """
        Converts a json string into a dictionary
        """
        return json.loads(config_str)
    
    def get(self, key):
        """
        Returns the value for a given key
        """
        return self.config[key]