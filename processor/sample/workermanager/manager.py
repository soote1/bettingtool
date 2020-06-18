import time
import logging
from multiprocessing import Event, Process, get_logger, log_to_stderr

from processor.sample.common.model import Worker, TimedWorker
from processor.sample.workermanager.helpers import ConfigHelper, WorkerFactory

class WorkerManager:
    PROCESSORS = "processors"
    WAIT_TIME = "wait_time"

    def __init__(self, config_file_path):
        """
        Initialize extractor instance.
        """
        log_to_stderr()
        self.logger = get_logger()
        self.logger.setLevel(logging.INFO)
        self.processors = []
        self.processes = []
        self.config_helper = ConfigHelper(config_file_path)
        self.load_config()

    
    def load_config(self):
        """
        Creates workers instances.
        """
        try:
            self.logger.info(f"loading WorkerManager config {self.config_helper.config}")
            self.load_processors()
        except Exception as error:
            self.logger.error(f"invalid configuration for {WorkerManager.__name__} class")
            self.logger.error(error)
            raise error


    def load_processors(self):
        """
        Creates processor instances.
        """
        processors_configurations = self.config_helper.get(WorkerManager.PROCESSORS)
        self.processors = WorkerFactory.create_instances(processors_configurations)

    def run(self):
        """
        Starts all processes and stop them when keyboard interrupt signal is received.
        """
        keyboard_interrupt_event = Event()
        worker_instances = self.processors
        # create processes
        for worker_instance in worker_instances:
            if isinstance(worker_instance, Worker):
                process = Process(target=worker_instance.run)
            if isinstance(worker_instance, TimedWorker):
                process = Process(target=worker_instance.run, args=(keyboard_interrupt_event,))
            self.processes.append(process)

        # start all processes
        for process in self.processes:
            process.start()

        while True:
            try:
                time.sleep(self.config_helper.get(WorkerManager.WAIT_TIME))
            except KeyboardInterrupt as error:
                self.logger.info("sending shutdown signal to child processes")
                keyboard_interrupt_event.set()
                break
        
        for process in self.processes:
            process.join()