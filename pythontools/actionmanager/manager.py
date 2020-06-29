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

    def __init__(self, config):
        """
        Prepares the action manager instance with a given configuration.
        An ActionManagerError is thrown if invalid config.
        """
        self.config = config
        self.validate_config()
    
    def validate_config(self):
        """
        Validates action manager configuration.
        An ActionManagerError is thrown if invalid config.
        """
        try:
            self.config[ActionManager.INITIAL_ACTION]
        except KeyError as error:
            raise ActionManagerError(f"Missing configuration key. {error}")

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
        output = data
        self.current_action = self.create_action(self.config[ActionManager.INITIAL_ACTION])
        try:
            while True:
                output = self.current_action.run(output)
                next_action_name = output[ActionManager.NEXT_ACTION]
                if not next_action_name:
                    break
                
                self.current_action = self.create_action(self.config[next_action_name])
            return True
        except KeyError:
            raise ActionManagerError(f"No action metadata for {next_action_name}")
        except ActionError as error:
            raise error
        except Exception:
            return False
    
    def create_action(self, action_metadata):
        """
        Returns a new object matching the given action's metadata.
        An ActionManagerError is thrown if can't create action instance.
        """
        try:
            action = ActionFactory.create_action(
                action_metadata[ActionManager.MODULE], 
                action_metadata[ActionManager.CLASS], 
                action_metadata[ActionManager.CONFIG]
            )
        except:
            raise ActionManagerError(f"Error while creating action instance using {action_metadata}")
        
        return action