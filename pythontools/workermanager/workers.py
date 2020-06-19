class Worker:
    """
    Abstract class to define the basic structure of 
    a specif type of worker.
    """
    def __init__(self):
        """
        Initialize worker instance.
        """
        raise NotImplementedError

    def run(self):
        """
        Logic to be executed on each iteration.
        """
        raise NotImplementedError
    
    def do_work(self):
        """
        Performs a specific type of work.
        """
        raise NotImplementedError

class TimedWorker(Worker):
    def __init__(self, wait_time):
        """
        Initialize timed worker class.
        """
        self.wait_time = wait_time

    def run(self, shutdown_event):
        """
        Calls do_work method inside an infinite loop and
        wait n seconds to receive a shutdown event before
        calling do_work again.
        """
        do_work = True
        while not shutdown_event.is_set():
            try:
                if do_work:
                    self.do_work()
                shutdown_event.wait(self.wait_time)
            except KeyboardInterrupt:
                do_work = False