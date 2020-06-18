import json
import importlib

class WorkerFactory(object):
    MODULE_ITEM = "module"
    CLASS_ITEM = "class"
    ARGS_ITEM = "args"

    @staticmethod
    def create_instance(module_str, class_name_str, args):
        """
        Creates a new instance of a given class from a given module and passes a list of arguments.
        """
        class_module = importlib.import_module(module_str)
        class_object = getattr(class_module, class_name_str)
        return class_object(*args)

    @staticmethod
    def create_instances(instance_config_list):
        """
        Creates a list of objects from a given list of object configurations
        """
        objects = []
        for instance_config in instance_config_list:
            # need to check if current instance needs to be created
            if WorkerFactory.MODULE_ITEM in instance_config:
                module_name = instance_config[WorkerFactory.MODULE_ITEM]
                class_name = instance_config[WorkerFactory.CLASS_ITEM]
                args_config_list = instance_config[WorkerFactory.ARGS_ITEM]
                args = []
                # create instances for all arguments recursively if any
                if len(args_config_list) > 0:
                    args.extend(WorkerFactory.create_instances(args_config_list))
                objects.append(WorkerFactory.create_instance(module_name, class_name, args))
            else:
                objects.append(instance_config)

        return objects

class ConfigHelper:
    def __init__(self, file_path):
        """
        Initialize config helper
        """
        self.config = self.parse_config(self.load_config_file(file_path))

    def parse_config(self, config_str):
        """
        Converts a json string into a dictionary
        """
        return json.loads(config_str)
    
    def get(self, key):
        """
        Returns the value for a given key
        """
        return self.config[key]

    def load_config_file(self, file_path):
        """
        Reads config file and returns it as a json string
        """
        with open(file_path) as file:
            config_str = file.read()

        return config_str
