from pythontools.actionmanager.helpers import ActionFactory
from pythontools.actionmanager.errors import ActionError, ActionManagerError

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
    MAX_ATTEMPS = "max_attempts"

    def __init__(self, config):
        """
        Prepares the action manager instance with a given configuration.
        An ActionManagerError is thrown if invalid config.
        """
        self.config = config
        self.load_config()
    
    def load_config(self):
        """
        Validates action manager configuration.
        An ActionManagerError is thrown if invalid config.
        """
        try:
            self.max_attempts = self.config[ActionManager.MAX_ATTEMPS]
            self.current_attempt = 0
            self.current_action = self.create_action(ActionManager.INITIAL_ACTION)
        except KeyError as error:
            raise ActionManagerError(f"Error while accesing action config. {error}")

    def run_workflow(self, data):
        """
        Executes a list of actions in sequential order, passing an input object as
        an argument. The argument received in the data param is the input for the
        initial action. From the second action until the end, the input object
        is the output of the previous action. The execution stops when the next_action
        key in the action config is an empty string.
        If the action manager can't read the next action, it throws an ActionManagerError.
        If the action manager receives an ActionError, it would stop the execution.
        If the action manager receives another type of exception, it would re-attempt the
        workflow from the beginning using the initial data. In this case, it stops when the
        maximum number of attempts is reached.
        """
        action_data = data
        try:
            while True:
                action_data = self.current_action.run(action_data)
                next_action_name = self.current_action.get_next_action()
                if not next_action_name:
                    break

                self.current_action = self.create_action(self.config[next_action_name])
            return True
        except KeyError:
            raise ActionManagerError(f"No action metadata for {next_action_name}")
        except ActionError as error:
            raise error
        except Exception:
            if self.current_attempt == self.max_attempts:
                return False
            else:
                self.re_attempt_workflow(data)

    def re_attempt_workflow(self, data):
        """
        Increments the current attempt and runs workflow again.
        """
        self.current_attempt += 1
        self.run_workflow(data)
    
    def create_action(self, action_name):
        """
        Returns a new object matching the given action's metadata.
        An ActionManagerError is thrown if can't create action instance.
        """
        if not self.config.get(action_name):
            raise ActionManagerError(f"No metadata found for name {action_name}")
        try:
            action = ActionFactory.create_action(
                self.config[action_name][ActionManager.MODULE], 
                self.config[action_name][ActionManager.CLASS], 
                self.config[action_name][ActionManager.CONFIG]
            )
        except:
            raise ActionManagerError(f"Error while creating action instance {self.config[action_name]}")
        
        return action