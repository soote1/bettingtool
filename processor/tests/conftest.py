import pytest

class ActionMock:
    def __init__(self, config):
        self.config = config

    def run(self, data):
        return data

class AnotherActionMock:
    def __init__(self, config):
        self.config = config
    
    def run(self, data):
        return data

def sample_config():
    return {"some_key":"some_value"}

@pytest.fixture
def action_metadata_mock():
    return {
        "module":"processor.tests.conftest",
        "class":"ActionMock",
        "config":{"some_key":"some_value"},
        "next_action":""
    }

@pytest.fixture
def action_object_mock():
    return ActionMock(sample_config())

@pytest.fixture
def action_manager_config_mock():
    return {
        "initial_action":{
            "module":"processor.tests.conftest",
            "class":"ActionMock",
            "config":{},
            "next_action":"another_action_mock"
        },
        "another_action_mock":{
            "module":"processor.tests.conftest",
            "class":"AnotherActionMock",
            "config":{},
            "next_action":""
        }
    }