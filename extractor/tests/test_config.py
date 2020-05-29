import pytest
import os
from extractor.sample.helpers.config import Config

class TestConfig:
    def test_create_config_dict(self):
        expected_output = {
            "producers":"",
            "consumers": "",
            "fetchers":"",
            "seeders":[["extractor.sample.model.caliente_seeder", "CalienteSeeder"]],
            "listeners":""
        }

        with open("/home/soote1/projects/bettingtool/extractor/sample/config.json") as file:
            config_str = file.read()
            
        config = Config(config_str)

        assert expected_output == config.config

    def test_get_value_from_config(self):
        expected_output = [["extractor.sample.model.caliente_seeder", "CalienteSeeder"]]

        with open("/home/soote1/projects/bettingtool/extractor/sample/config.json") as file:
            config_str = file.read()
            
        config = Config(config_str)
        output = config.get("seeders")
        assert expected_output == output
