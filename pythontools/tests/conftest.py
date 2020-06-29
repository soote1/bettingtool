import pytest

from pythontools.workermanager.workers import TimedWorker, Worker
from pythontools.actionmanager.actions import BaseAction
from pythontools.actionmanager.errors import ActionError

class WorkerMock(Worker):
    def __init__(self, config):
        self.config = config

    def run(self):
        return

    def do_work(self):
        return

class TimedWorkerMock(TimedWorker):
    def __init__(self, config):
        super().__init__(config)

    def do_work(self):
        return

class ClassWithRunMethod:
    def __init__(self, config):
        self.config = config    
    def run(self):
        return

class InvalidWorkerType:
    def __init__(self, config):
        self.config = config
    
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
                "class":"TimedWorkerMock",
                "args":[{"wait_time":1}]
            },
            {
                "module":"pythontools.tests.conftest",
                "class":"ClassWithRunMethod",
                "args":[{"wait_time":1}]
            }
        ]
    }

@pytest.fixture
def worker_manager_config_invalid_worker_type():
    return {
        "wait_time":5,
        "workers":[
            {
                "module":"pythontools.tests.conftest",
                "class":"TimedWorkerMock",
                "args":[{"wait_time":1}]
            },
            {
                "module":"pythontools.tests.conftest",
                "class":"InvalidWorkerType",
                "args":[{"wait_time":1}]
            }
        ]
    }

@pytest.fixture
def worker_manager_config_invalid_worker_metadata():
    return {
        "wait_time":5,
        "workers":[
            {
                "module":"pythontools.tests.conftest",
                "class":"TimedWorkerMock",
                "args":[{"wait_time":1}]
            },
            {
                "module":"pythontools.tests.conftest",
                "class":"UnexistingClass",
                "args":[{"wait_time":1}]
            }
        ]
    }

class ActionMock(BaseAction):
    def __init__(self, config):
        super().__init__(config)

    def run(self, data):
        data["next_action"] = self.config["next_action"]
        return data

class AnotherActionMock(BaseAction):
    def __init__(self, config):
        super().__init__(config)

    def run(self, data):
        data["next_action"] = self.config["next_action"]
        return data

class ExceptionAction(BaseAction):
    def run(self, data):
        raise ActionError("Action error")

class ReAttemptAction(BaseAction):
    def run(self, data):
        raise Exception("Some error")

def sample_config():
    return {"some_key":"some_value", "next_action":""}

@pytest.fixture
def action_metadata_mock():
    return {
        "module":"pythontools.tests.conftest",
        "class":"ActionMock",
        "config":{"some_key":"some_value", "next_action":""}
    }

@pytest.fixture
def action_object_mock():
    return ActionMock(sample_config())

@pytest.fixture
def action_manager_config_mock():
    return {
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
        "initial_action":{
            "module":"pythontools.tests.conftest",
            "class":"ExceptionAction",
            "config":{"next_action":"another_action_mock"}
        }
    }

@pytest.fixture
def action_manager_config_reattempt_mock():
    return {
        "initial_action":{
            "module":"pythontools.tests.conftest",
            "class":"ReAttemptAction",
            "config":{"next_action":"another_action_mock"}
        }
    }