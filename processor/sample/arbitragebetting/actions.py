from processor.sample.actionmanager.actions import BaseAction

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
    An action to filter games with incomplete scores
    """
    def __init__(self, config):
        super().__init__(config)

    def run(self, data):
        return data