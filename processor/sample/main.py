import os

from processor.sample.workermanager.manager import WorkerManager

worker_manager = WorkerManager(f"{os.path.dirname(__file__)}/config.json")
worker_manager.run()
