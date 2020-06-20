import os
import json
from multiprocessing import log_to_stderr

from pythontools.workermanager.manager import WorkerManager

log_to_stderr()

with open(f"{os.path.dirname(__file__)}/config.json") as file:
    config = json.loads(file.read())

worker_manager = WorkerManager(config)
worker_manager.run()
