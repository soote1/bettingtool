from multiprocessing import get_logger

from extractor.sample.workers.worker import Worker

class TimedWorker(Worker):
    def __init__(self, wait_time):
        """
        Initialize timed worker class.
        """
        self.logger = get_logger()
        self.wait_time = wait_time
        self.current_state = "new"

    def run(self, shutdown_event):
        """
        Calls do_work method inside an infinite loop and
        wait n seconds to receive a shutdown event before
        calling do_work again.
        """
        while not shutdown_event.is_set():
            try:
                self.do_work()
                shutdown_event.wait(self.wait_time)
            except KeyboardInterrupt as error:
                continue
    
    def do_work(self):
        raise NotImplementedError