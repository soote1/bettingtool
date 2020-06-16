import os
import json

from processor.sample.actionmanager.manager import ActionManager

with open(f"{os.path.dirname(__file__)}/config.json") as file:
    config_str = file.read()

config_dict = json.loads(config_str)
action_manager = ActionManager(config_dict["arbitrage_betting_processor"])
success = action_manager.run_workflow({"some_key":"some_value"})