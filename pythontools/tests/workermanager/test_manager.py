from multiprocessing import Process

from pythontools.workermanager.manager import WorkerManager
from pythontools.workermanager.errors import WorkerManagerError
from pythontools.tests.conftest import WorkerMock

class TestWorkerManager:
    """
    Tests worker manager's core functionalities
    """
    def get_manager_and_workers(self, worker_manager_config):
        worker_manager = WorkerManager(worker_manager_config)
        return (worker_manager, worker_manager.create_workers(worker_manager.workers_config_list))

    def get_manager_and_processes(self, worker_manager_config):
        worker_manager, workers = self.get_manager_and_workers(worker_manager_config)
        processes = worker_manager.create_processes(workers)
        return (worker_manager, processes)

    def create_and_start_processes(self, worker_manager_config):
        worker_manager, processes = self.get_manager_and_processes(worker_manager_config)
        worker_manager.start_processes(processes)

        return (worker_manager, processes)

    def validate_proccesses_are_alive(self, worker_manager, processes):
        for process in processes:
            assert process.is_alive()
        worker_manager.stop_processes(processes)

    def test_create_and_load_config(self, worker_manager_config):
        worker_manager = WorkerManager(worker_manager_config)
        assert worker_manager.wait_time == worker_manager_config["wait_time"]
        assert worker_manager.workers_config_list == worker_manager_config["workers"]

    def test_create_manager_with_invalid_config(self):
        try:
            WorkerManager({})
            assert False
        except WorkerManagerError:
            assert True

    def test_create_workers(self, worker_manager_config):
        workers = self.get_manager_and_workers(worker_manager_config)[1]
        for worker in workers:
            assert isinstance(worker, WorkerMock)

    def test_create_workers_invalid_worker_metadata(self, worker_manager_config_invalid_worker_metadata):
        try:
            self.get_manager_and_workers(worker_manager_config_invalid_worker_metadata)[1]
            assert False
        except WorkerManagerError:
            assert True

    def test_create_processes(self, worker_manager_config):
        processes = self.get_manager_and_processes(worker_manager_config)[1]
        assert len(processes) == len(worker_manager_config["workers"])
        for process in processes:
            assert isinstance(process, Process)

    def test_create_processes_with_invalid_worker_type(self, worker_manager_config_invalid_worker_type):
        try:
            self.get_manager_and_processes(worker_manager_config_invalid_worker_type)[1]
            assert False
        except WorkerManagerError:
            assert True

    def test_start_processes(self, worker_manager_config):
        worker_manager, processes = self.create_and_start_processes(worker_manager_config)
        self.validate_proccesses_are_alive(worker_manager, processes)

    def test_stop_processes(self, worker_manager_config):
        worker_manager, processes = self.create_and_start_processes(worker_manager_config)
        self.validate_proccesses_are_alive(worker_manager, processes)
        for process in processes:
            assert not process.is_alive()