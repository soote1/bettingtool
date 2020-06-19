class BaseAction:
    NEXT_ACTION = "next_action"
    """
    Base action
    """
    def __init__(self, action_config):
        self.config = action_config

    def run(self, data):
        raise NotImplementedError
    
    def get_next_action(self):
        return self.config[BaseAction.NEXT_ACTION]