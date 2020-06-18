from processor.sample.actionmanager.manager import ActionManager

class TestActionManager:
    def test_run_workflow(self, action_manager_config_mock):
        """
        Should execute action manager workflow and
        return the result object
        """
        action_manager = ActionManager(action_manager_config_mock)
        successful_result = action_manager.run_workflow({"some":"data"})

        assert successful_result
        