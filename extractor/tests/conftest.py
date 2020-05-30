import pytest
import os

@pytest.fixture
def config_str():
    config_file_path = f"{os.path.dirname(__file__).replace('tests', 'sample')}/config.json"

    with open(config_file_path) as file:
            config_str = file.read()
    return config_str  