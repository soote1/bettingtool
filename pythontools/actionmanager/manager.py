from pythontools.actionmanager.helpers import ActionFactory

class ActionManager:
    """
    A generic class to perform a set of actions
    to a given object
    """

    MODULE = "module"
    CLASS = "class"
    CONFIG = "config"
    NEXT_ACTION = "next_action"
    INITIAL_ACTION = "initial_action"

    def __init__(self, config):
        """
        Prepares the action manager instance with a given configuration.
        """
        self.config = config

    def run_workflow(self, data):
        """
        Executes a list of actions in secuencial order, passing an input object as
        argument. The argument received in the data param is the input for the
        initial action. From the second action until the end, the input object
        is the output of the previous action. The execution stops when the next_action
        property in the action config is set to an empty string.
        """
        action_data = data
        action_metadata = self.config[ActionManager.INITIAL_ACTION]
        current_action = self.create_action(action_metadata)
        while True:
            try:
                action_data = current_action.run(action_data)
                next_action = action_metadata[ActionManager.NEXT_ACTION]
                if not next_action:
                    break

                action_metadata = self.config[next_action]
                current_action = self.create_action(action_metadata)
            except Exception as error:
                # TODO: handle error propperly
                return False
        # TODO: improve return value
        return True
    
    def create_action(self, action_metadata):
        """
        Returns a new object matching the given action's metadata.
        """
        return ActionFactory.create_action(
            action_metadata[ActionManager.MODULE], 
            action_metadata[ActionManager.CLASS], 
            action_metadata[ActionManager.CONFIG]
        )