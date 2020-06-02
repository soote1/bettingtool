from multiprocessing import Event, get_logger
import time
import os

from extractor.sample.helpers.cache_client import CacheClient

class Worker:
    def __init__(self, name, wait_time):
        self.name = name
        self.logger = get_logger()
        self.wait_time = wait_time
        self.current_state = "new"

    def run(self, shutdown_event):
        while not shutdown_event.is_set():
            try:
                self.do_work()
                time.sleep(self.wait_time)
            except KeyboardInterrupt as error:
                continue
    
    def do_work(self):
        raise NotImplementedError

    def get_state(self):
        return self.current_state

    def update_state(self, state):
        self.current_state = state