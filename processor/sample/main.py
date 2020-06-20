import os
import json

from pythontools.workermanager.manager import WorkerManager

with open(f"{os.path.dirname(__file__)}/config.json") as file:
    config = json.loads(file.read())

worker_manager = WorkerManager(config)
worker_manager.run()
