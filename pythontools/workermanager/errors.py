class Error(Exception):
    """
    Base class for exceptions in this package
    """

class WorkerError(Error):
    """
    Base class for worker exceptions
    """
    def __init__(self, message):
        self.message = message

class WorkerManagerError(Error):
    """
    Raised when the worker manager has an error
    """
    def __init__(self, message):
        self.message = message