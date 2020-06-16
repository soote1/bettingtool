import importlib

class ActionFactory:
    """
    A static class to handle action creation
    """
    @staticmethod
    def create_action(module_name, class_name, config):
        """
        Generic method to create an action object
        """
        class_module = importlib.import_module(module_name)
        class_object = getattr(class_module, class_name)
        return class_object(config)