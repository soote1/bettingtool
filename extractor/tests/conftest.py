import pytest
import os

class SimpleObject:
    def __init__(self, arg1, arg2, arg3):
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3

class NestedObject:
    def __init__(self, arg1, arg2, arg3):
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3

@pytest.fixture
def config_str():
        """
        Creates a mock object for the app configuration using the original config.json file
        """
        config_file_path = f"{os.path.dirname(__file__).replace('tests', 'sample')}/config.json"
        with open(config_file_path) as file:
            config_str = file.read()
        return config_str

@pytest.fixture
def simple_object():
    return SimpleObject("arg1", "arg2", "arg3")

@pytest.fixture
def simple_object_metadata():
    return {
        "module":"extractor.tests.conftest",
        "class":"SimpleObject",
        "args":[
            "arg1",
            "arg2",
            "arg3"
        ]
    }

@pytest.fixture
def simple_object_metadata_list():
    return [
        {
            "module":"extractor.tests.conftest",
            "class":"SimpleObject",
            "args":[
                "arg1",
                "arg2",
                "arg3"
            ]
        },
        {
            "module":"extractor.tests.conftest",
            "class":"SimpleObject",
            "args":[
                "a",
                "b",
                "c"
            ]
        }
    ]

@pytest.fixture
def nested_object_metadata_list():
    return [
        {
            "module":"extractor.tests.conftest",
            "class":"NestedObject",
            "args":[
                {
                    "module":"extractor.tests.conftest",
                    "class":"SimpleObject",
                    "args":[
                        "a",
                        "b",
                        "c"
                    ]
                },
                "arg2",
                "arg3"
            ]
        }
    ]