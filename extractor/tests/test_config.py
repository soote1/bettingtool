import pytest
import os
from extractor.sample.helpers.config import Config

def test_should_create_config_dict():
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

