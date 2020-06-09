from multiprocessing import Event, get_logger

class Game(dict):
    def __init__(self, game_id, game_type, odds):
        self.game_id = game_id
        self.game_type = game_type
        self.odds = odds

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

    def run(self, shutdown_event):
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
    def __init__(self, wait_time, wait_first=False):
        """
        Initialize timed worker class.
        """
        self.logger = get_logger()
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
            except KeyboardInterrupt as error:
                do_work = False
    
    def do_work(self):
        raise NotImplementedError

class Fetcher:
    def __init__(self):
        pass

    def fetch(self):
        pass

class Seeder(TimedWorker):
    """
    Abstract class to represent seeder worker type.
    """
    def __init__(self, wait_time):
        """
        Initialize seeder instance.
        """
        super().__init__(wait_time)
