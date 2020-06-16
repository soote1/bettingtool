class BaseAction:
    """
    Base action
    """
    def __init__(self, action_config):
        self.config = action_config

    def run(self, data):
        raise NotImplementedError
    
    def get_next_action(self):
        return self.config["next_action"]

class DuplicateFilter(BaseAction):
    """
    An action to filter duplicate odds
    """
    def __init__(self, config):
        super().__init__(config)

    def run(self, data):
        return data

class IncompleteScoresFilter(BaseAction):
    """
    An action to filter filter games with incomplete scores
    """
    def __init__(self, config):
        super().__init__(config)

    def run(self, data):
        return data