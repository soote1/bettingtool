from multiprocessing import Process

from pythontools.workermanager.manager import WorkerManager
from pythontools.tests.conftest import WorkerMock

class TestWorkerManager:
    def test_create_and_load_config(self, worker_manager_config):
        worker_manager = WorkerManager(worker_manager_config)
        assert worker_manager.wait_time == worker_manager_config["wait_time"]
        assert worker_manager.workers_config_list == worker_manager_config["workers"]

    def test_create_workers(self, worker_manager_config):
        worker_manager = WorkerManager(worker_manager_config)
        workers = worker_manager.create_workers(worker_manager.workers_config_list)
        for worker in workers:
            assert isinstance(worker, WorkerMock)

    def test_create_processes(self, worker_manager_config):
        worker_manager = WorkerManager(worker_manager_config)
        workers = worker_manager.create_workers(worker_manager.workers_config_list)
        processes = worker_manager.create_processes(workers)
        assert len(processes) == len(worker_manager_config["workers"])
        for process in processes:
            assert isinstance(process, Process)

    def test_start_processes(self, worker_manager_config):
        worker_manager = WorkerManager(worker_manager_config)
        workers = worker_manager.create_workers(worker_manager.workers_config_list)
        processes = worker_manager.create_processes(workers)
        worker_manager.start_processes(processes)
        for process in processes:
            assert process.is_alive()

    def test_stop_processes(self, worker_manager_config):
        worker_manager = WorkerManager(worker_manager_config)
        workers = worker_manager.create_workers(worker_manager.workers_config_list)
        processes = worker_manager.create_processes(workers)
        worker_manager.start_processes(processes)
        for process in processes:
            assert process.is_alive()
        worker_manager.stop_processes(processes)
        for process in processes:
            assert not process.is_alive()