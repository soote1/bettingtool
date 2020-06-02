import pytest
import os
import json
from extractor.sample.config.config import Config

class TestConfig:    
    def test_create_config_dict(self, config_str):
        config_mock = json.loads(config_str)
        config = Config(config_str)

        assert config_mock == config.config

    def test_get_value_from_config(self, config_str):         
        key = "seeders"
        config_mock = json.loads(config_str)
        config = Config(config_str)
        output = config.get(key)
        assert config_mock[key] == output
