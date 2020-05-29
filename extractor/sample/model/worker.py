from multiprocessing import Event
import time

class Worker:
    def __init__(self, wait_time):
        raise NotImplementedError

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
        raise NotImplementedError

    def update_state(self):
        raise NotImplementedError