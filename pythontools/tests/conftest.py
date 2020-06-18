import pytest

from pythontools.workermanager.workers import TimedWorker

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