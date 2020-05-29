import importlib

class WorkerFactory(object):
    @staticmethod
    def create_instance(module_str, class_name_str, wait_time=0):
        """
        Creates a new instance of a given class from a given module
        """
        class_module = importlib.import_module(module_str)
        class_object = getattr(class_module, class_name_str)
        
        return class_object(wait_time)
