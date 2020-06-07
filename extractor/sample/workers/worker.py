from multiprocessing import Event, get_logger
import time
import os

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