import pytest
import os
import json
from extractor.sample.common.helpers import ConfigHelper, WorkerFactory

class TestConfig:
    """
    ConfigHelper test suite
    """
    config_file_path = f"{os.path.dirname(__file__).replace('tests', 'sample').replace('common', '')}/config.json"

    def test_create_config_dict(self, config_str):
        """
        Tests that the ConfigHelper is able to create the config dict 
        from a config string.
        """
        config_mock = json.loads(config_str)
        config = ConfigHelper(TestConfig.config_file_path)

        assert config_mock == config.config

    def test_get_value_from_config(self, config_str):
        """
        Tests that the ConfigHelper is able to retrieve the 
        corresponding value for a given key
        """   
        key = "seeders"
        config_mock = json.loads(config_str)
        config = ConfigHelper(TestConfig.config_file_path)
        output = config.get(key)
        assert config_mock[key] == output

class TestWorkerFactory:
    """
    WorkerFactory test suite
    """
    def test_create_instance(self, simple_object, simple_object_metadata):
        """
        Tests that the WorkerFactory is able to create an
        object from a given module name, class name and a
        list of argument objects
        """
        expected_arg1 = simple_object.arg1
        expected_arg2 = simple_object.arg2
        expected_arg3 = simple_object.arg3

        obj = WorkerFactory.create_instance(
            simple_object_metadata["module"], 
            simple_object_metadata["class"], 
            simple_object_metadata["args"]
        )

        assert type(simple_object) == type(obj)
        assert expected_arg1 == obj.arg1
        assert expected_arg2 == obj.arg2
        assert expected_arg3 == obj.arg3

    def test_create_multiple_instances(self, simple_object_metadata_list):
        """
        Tests that the WorkerFactory is able to create
        a list of several objects from a list of config
        dictionaries
        """
        objects = WorkerFactory.create_instances(simple_object_metadata_list)
        assert len(objects) == len(simple_object_metadata_list)

    def test_create_multiple_instances_nested_arguments(self, nested_object_metadata_list):
        """
        Tests that the WorkerFactory is able to create
        a list of several objects from a list of config
        dictionaries with nested arguments
        """
        objects = WorkerFactory.create_instances(nested_object_metadata_list)
        assert len(objects) == len(nested_object_metadata_list)
