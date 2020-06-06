from multiprocessing import Event, get_logger
import time
import os

class Worker:
    def __init__(self, name, wait_time):
        """
        Initialize worker.
        """
        self.name = name
        self.logger = get_logger()
        self.wait_time = wait_time
        self.current_state = "new"

    def run(self, shutdown_event):
        """
        Calls do_work method inside an infinite loop and 
        listens for a shutdown event to break the loop.
        """
        while not shutdown_event.is_set():
            try:
                self.do_work()
                time.sleep(self.wait_time)
            except KeyboardInterrupt as error:
                continue
    
    def do_work(self):
        raise NotImplementedError