class Error(Exception):
    """
    Base class for exceptions in this package
    """

class ActionError(Error):
    """
    Base class for action exceptions
    """
    def __init__(self, message):
        self.message = message

class ActionManagerError(Error):
    """
    Raised when the action manager has an error
    """
    def __init__(self, message):
        self.message = message