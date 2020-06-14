import os
import logging
import time

from multiprocessing import Event, Process, get_logger, log_to_stderr
from extractor.sample.common.model import TimedWorker, Worker
from extractor.sample.common.helpers import WorkerFactory, ConfigHelper

class Extractor:
    CONSUMERS = "consumers"
    SEEDERS = "seeders"
    TOOLS = "tools"
    WAIT_TIME = "wait_time"

    def __init__(self, config_file_path):
        """
        Initialize extractor instance.
        """
        log_to_stderr()
        self.logger = get_logger()
        self.logger.setLevel(logging.INFO)
        self.consumers = []
        self.seeders = []
        self.tools = []
        self.processes = []
        self.config_helper = ConfigHelper(config_file_path)
        self.load_config()

    
    def load_config(self):
        """
        Creates workers instances.
        """
        try:
            self.logger.info(f"Loading extractor config {self.config_helper.config}")
            self.load_consumers()
            self.load_seeders()
            self.load_tools()
        except Exception as error:
            self.logger.error(f"Invalid configuration for {Extractor.__name__} class")
            self.logger.error(error)
            raise error


    def load_seeders(self):
        """
        Creates seeder instances.
        """
        seeders_configurations = self.config_helper.get(Extractor.SEEDERS)
        self.seeders = WorkerFactory.create_instances(seeders_configurations)

    def load_consumers(self):
        """
        Creates consumer instances.
        """
        consumers_configurations = self.config_helper.get(Extractor.CONSUMERS)
        self.consumers = WorkerFactory.create_instances(consumers_configurations)
    
    def load_tools(self):
        """
        Creates tools instances.
        """
        tools_configurations = self.config_helper.get(Extractor.TOOLS)
        self.tools = WorkerFactory.create_instances(tools_configurations)

    def run(self):
        """
        Starts all processes and stop them when keyboard interrupt signal is received.
        """
        keyboard_interrupt_event = Event()
        worker_instances =self.tools + self.consumers + self.seeders
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
                time.sleep(self.config_helper.get(Extractor.WAIT_TIME))
            except KeyboardInterrupt as error:
                self.logger.info("sending shutdown signal to child processes")
                keyboard_interrupt_event.set()
                break
        
        for process in self.processes:
            process.join()