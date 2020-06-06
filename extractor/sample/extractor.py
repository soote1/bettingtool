import json
import logging
import time
from multiprocessing import Event, Process, get_logger, log_to_stderr

from extractor.sample.config.config_keys import ConfigKeys
from extractor.sample.config.config_helper import ConfigHelper
from extractor.sample.workers.worker_factory import WorkerFactory

class Extractor:
    def __init__(self, config_helper):
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
        self.config_helper = config_helper
        self.load_config()
    
    def load_config(self):
        """
        Creates workers instances.
        """
        self.logger.info(f"Loading extractor config {self.config_helper.config}")
        self.load_consumers()
        self.load_seeders()
        self.load_tools()

    def load_seeders(self):
        """
        Creates seeder instances.
        """
        seeders_configurations = self.config_helper.get(ConfigKeys.seeders())
        self.seeders = WorkerFactory.create_instances(seeders_configurations)

    def load_consumers(self):
        """
        Creates consumer instances.
        """
        consumers_configurations = self.config_helper.get(ConfigKeys.consumers())
        self.consumers = WorkerFactory.create_instances(consumers_configurations)
    
    def load_tools(self):
        """
        Creates tools instances.
        """
        tools_configurations = self.config_helper.get(ConfigKeys.tools())
        self.tools = WorkerFactory.create_instances(tools_configurations)

    def run(self):
        """
        Starts all processes and stop them when keyboard interrupt signal is received.
        """
        keyboard_interrupt_event = Event()
        worker_instances = self.consumers + self.seeders + self.tools
        # create processes
        for worker_instance in worker_instances:
            process = Process(target=worker_instance.run, args=(keyboard_interrupt_event,))
            self.processes.append(process)

        # start all processes
        for process in self.processes:
            process.start()

        while True:
            try:
                time.sleep(self.config_helper.get(ConfigKeys.wait_time()))
            except KeyboardInterrupt as error:
                self.logger.info("sending shutdown signal to child processes")
                keyboard_interrupt_event.set()
                break
        
        for process in self.processes:
            process.join()

