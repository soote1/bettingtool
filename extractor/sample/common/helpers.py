import importlib
import json
from multiprocessing import get_logger

import requests
from bs4 import BeautifulSoup

class RequestsHelper:
    """
    Basic wrapper for requests library
    """
    def __init__(self, *args):
        self.logger = get_logger()

    def get(self, url):
        self.logger.info(f"performing GET request to {url}")
        return requests.get(url)

class HtmlParserHelper:
    def __init__(self, *args):
        self.logger = get_logger()
    
    def create_html_object(self, html_str, html_parser):
        self.logger.info(f"creating html object using {html_parser} parser")
        return BeautifulSoup(html_str, html_parser)

class WorkerFactory(object):
    MODULE_ITEM = "module"
    CLASS_ITEM = "class"
    CONFIG_ITEM = "config"
    DEPENDENCIES_ITEM = "dependencies"

    @staticmethod
    def create_instance(module_str, class_name_str, config=None, args=[]):
        """
        Creates a new instance of a given class from a given module and passes a config dict.
        """
        class_module = importlib.import_module(module_str)
        class_object = getattr(class_module, class_name_str)

        if config:
            return class_object(config, *args)
        else:
            return class_object(*args)

    @staticmethod
    def create_instances(instance_config_list):
        """
        Creates a list of objects from a given list of object configurations
        """
        objects = []
        for instance_config in instance_config_list:
            module_name = instance_config[WorkerFactory.MODULE_ITEM]
            class_name = instance_config[WorkerFactory.CLASS_ITEM]
            config = instance_config[WorkerFactory.CONFIG_ITEM]
            dependency_config_list = instance_config[WorkerFactory.DEPENDENCIES_ITEM]
            dependencies = []
            if len(dependency_config_list) > 0:
                dependencies.extend(WorkerFactory.create_instances(dependency_config_list))
            objects.append(WorkerFactory.create_instance(module_name, class_name, config, dependencies))

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