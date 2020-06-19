from pythontools.actionmanager.helpers import ActionFactory

class TestActionFactory:
    def test_create_action(self, action_metadata_mock, action_object_mock):
        """
        Should create an ActionMock instance.
        """
        action = ActionFactory.create_action(
            action_metadata_mock["module"], 
            action_metadata_mock["class"], 
            action_metadata_mock["config"]
        )

        assert type(action) == type(action_object_mock)
        assert action.config == action_object_mock.config