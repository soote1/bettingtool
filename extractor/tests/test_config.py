import pytest
import os
from extractor.sample.helpers.config import Config

class TestConfig:
    config_file_path = f"{os.path.dirname(__file__).replace('tests', 'sample')}/config.json"
    config_mock = {
            "producers":"",
            "consumers": "",
            "fetchers":"",
            "seeders":[["extractor.sample.model.caliente_seeder", "CalienteSeeder"]],
            "listeners":""
    }

    def read_config_from_file(self):
        with open(self.config_file_path) as file:
            config_str = file.read()
        return config_str     

    def test_create_config_dict(self):
        config = Config(self.read_config_from_file())

        assert self.config_mock == config.config

    def test_get_value_from_config(self):         
        key = "seeders"   
        config = Config(self.read_config_from_file())
        output = config.get(key)
        assert self.config_mock[key] == output
