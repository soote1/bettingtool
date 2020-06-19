from pythontools.actionmanager.manager import ActionManager
from pythontools.actionmanager.actions import BaseAction
from pythontools.actionmanager.errors import ActionManagerError, ActionError

class TestActionManager:
    """
    Unit tests suite for action manager
    """
    def test_create_manager(self, action_manager_config_mock):
        ActionManager(action_manager_config_mock)

    def test_create_manager_invalid_config(self):
        try:
            ActionManager({})
            assert False
        except ActionManagerError:
            assert True

    def test_create_action(self, action_manager_config_mock):
        action_manager = ActionManager(action_manager_config_mock)
        action = action_manager.create_action("initial_action")
        assert isinstance(action, BaseAction)
    
    def test_create_action_invalid_name(self, action_manager_config_mock):
        try:
            action_manager = ActionManager(action_manager_config_mock)
            action_manager.create_action("")
            assert False
        except ActionManagerError:
            assert True

    def test_create_action_invalid_action_metadata(self, action_manager_config_mock):
        try:
            action_manager_config_mock["initial_action"] = {}
            action_manager = ActionManager(action_manager_config_mock)
            action_manager.create_action("inital_action")
            assert False
        except ActionManagerError:
            assert True

    def test_run_workflow(self, action_manager_config_mock):
        """
        Should execute action manager workflow and
        return the result object
        """
        action_manager = ActionManager(action_manager_config_mock)
        action_manager.run_workflow({})

    def test_run_workflow_with_invalid_next_action(self, action_manager_config_mock):
        """
        Should execute action manager workflow and
        return the result object
        """
        try:
            action_manager_config_mock["initial_action"]["config"]["next_action"] = "invalid_name"
            action_manager = ActionManager(action_manager_config_mock)
            action_manager.run_workflow({})
            assert False
        except ActionManagerError:
            assert True
    
    def test_action_error(self, action_manager_config_exception_mock):
        """
        Should execute action manager workflow and
        return the result object
        """
        try:
            action_manager = ActionManager(action_manager_config_exception_mock)
            action_manager.run_workflow({})
            assert False
        except ActionError:
            assert True
    
    def test_re_attempt_workflow(self, action_manager_config_reattempt_mock):
        """
        Should execute action manager workflow and
        return the result object
        """
        action_manager = ActionManager(action_manager_config_reattempt_mock)
        success = action_manager.run_workflow({})
        assert not success
        assert action_manager.current_attempt == action_manager_config_reattempt_mock["max_attempts"]
