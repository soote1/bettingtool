import time
import logging
from multiprocessing import Event, Process, get_logger

from pythontools.workermanager.workers import Worker, TimedWorker
from pythontools.workermanager.helpers import WorkerFactory
from pythontools.workermanager.errors import WorkerManagerError

class WorkerManager:
    WORKERS = "workers"
    WAIT_TIME = "wait_time"

    def __init__(self, config):
        """
        Initializes manager's instance variables.
        """
        self.logger = get_logger()
        self.logger.setLevel(logging.INFO)
        self.wait_time = -1
        self.workers_config_list = []
        self.load_config(config)

    
    def load_config(self, config):
        """
        Checks that the configuration contains the keys
        for wait time value, and workers config list so that
        it can load the values into instance's variables.
        """
        try:
            self.logger.info(f"loading {self.__class__.__name__} config => {config}")
            self.wait_time = config[WorkerManager.WAIT_TIME]
            self.workers_config_list = config[WorkerManager.WORKERS]
        except KeyError as error:
            raise WorkerManagerError(f"Invalid configuration for worker manager => {error}")
        

    def create_workers(self, workers_config_list):
        """
        Creates a list of worker instances from a given worker config list 
        using WorkerFactory helper.
        """
        try:
            return WorkerFactory.create_instances(workers_config_list)
        except Exception:
            raise WorkerManagerError("Invalid worker metadata in workers configuration key")

    def create_processes(self, worker_instances, keyboard_interrupt_event=None):
        """
        Creates a list of Process objects and binds a worker instance to each object.
        """
        processes = []
        for worker_instance in worker_instances:
            if isinstance(worker_instance, Worker):
                process = Process(target=worker_instance.run)
            if isinstance(worker_instance, TimedWorker):
                process = Process(target=worker_instance.run, args=(keyboard_interrupt_event,))
                processes.append(process)
            else:
                raise WorkerManagerError(f"Invalid worker type received => {type(worker_instance)}")
        return processes

    def start_processes(self, processes):
        """
        Starts a list of processes
        """
        for process in processes:
            process.start()

    def stop_processes(self, processes):
        """
        Sotps a list of processes
        """
        for process in processes:
            process.join()

    def run(self):
        """
        Starts a list of processes and stop them when keyboard interrupt signal is received.
        """
        # create worker instances
        worker_instances = self.create_workers(self.workers_config_list)
        # create shutdown event
        keyboard_interrupt_event = Event()
        # create processes
        processes = self.create_processes(worker_instances, keyboard_interrupt_event)
        # start all processes
        self.start_processes(processes)

        # wait for KeyboardInterrupt error
        while True:
            try:
                time.sleep(self.wait_time)
            except KeyboardInterrupt:
                self.logger.info("sending shutdown signal to child processes")
                keyboard_interrupt_event.set()
                break

        # kill the processes
        self.stop_processes(processes)