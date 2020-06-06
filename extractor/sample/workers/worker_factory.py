import importlib
import json
from extractor.sample.config.config_keys import ConfigKeys

class WorkerFactory(object):
    @staticmethod
    def create_instance(module_str, class_name_str, config):
        """
        Creates a new instance of a given class from a given module and passes a config dict.
        """
        class_module = importlib.import_module(module_str)
        class_object = getattr(class_module, class_name_str)        
        return class_object(config)

    @staticmethod
    def create_instances(instance_config_list):
        """
        Creates a list of objects from a given list of object configurations
        """
        objects = []
        for instance_config in instance_config_list:
            module_name = instance_config[ConfigKeys.worker_module()]
            class_name = instance_config[ConfigKeys.worker_class()]
            config = instance_config[ConfigKeys.worker_config()]
            objects.append(WorkerFactory.create_instance(module_name, class_name, config))

        return objects
