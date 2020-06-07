from extractor.sample.workers.timed_worker import TimedWorker

class Seeder(TimedWorker):
    """
    Abstract class to represent seeder worker type.
    """
    def __init__(self, wait_time):
        """
        Initialize seeder instance.
        """
        super().__init__(wait_time)
