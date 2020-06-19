import pytest

from pythontools.workermanager.workers import TimedWorker
from pythontools.actionmanager.actions import BaseAction
from pythontools.actionmanager.errors import ActionError

class WorkerMock(TimedWorker):
    def __init__(self, config):
        super().__init__(config)

    def do_work(self):
        return

@pytest.fixture
def worker_manager_config():
    return {
        "wait_time":5,
        "workers":[
            {
                "module":"pythontools.tests.conftest",
                "class":"WorkerMock",
                "args":[{"wait_time":1}]
            },
            {
                "module":"pythontools.tests.conftest",
                "class":"WorkerMock",
                "args":[{"wait_time":1}]
            }
        ]
    }

class ActionMock(BaseAction):
    def run(self, data):
        return data

class AnotherActionMock(BaseAction):
    def run(self, data):
        return data

class ExceptionAction(BaseAction):
    def run(self, data):
        raise ActionError("Action error")

class ReAttemptAction(BaseAction):
    def run(self, data):
        raise Exception("Some error")

def sample_config():
    return {"some_key":"some_value"}

@pytest.fixture
def action_metadata_mock():
    return {
        "module":"pythontools.tests.conftest",
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
        "max_attempts":2,
        "initial_action":{
            "module":"pythontools.tests.conftest",
            "class":"ActionMock",
            "config":{"next_action":"another_action_mock"}
        },
        "another_action_mock":{
            "module":"pythontools.tests.conftest",
            "class":"AnotherActionMock",
            "config":{"next_action":""}
        }
    }

@pytest.fixture
def action_manager_config_exception_mock():
    return {
        "max_attempts":2,
        "initial_action":{
            "module":"pythontools.tests.conftest",
            "class":"ExceptionAction",
            "config":{"next_action":"another_action_mock"}
        }
    }

@pytest.fixture
def action_manager_config_reattempt_mock():
    return {
        "max_attempts":2,
        "initial_action":{
            "module":"pythontools.tests.conftest",
            "class":"ReAttemptAction",
            "config":{"next_action":"another_action_mock"}
        }
    }