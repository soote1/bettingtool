from extractor.sample.workers.worker_factory import WorkerFactory
from extractor.sample.config.config import Config
from extractor.sample.extractor import Extractor
import os

with open(f"{os.path.dirname(__file__)}/config.json") as file:
    config_str = file.read()

config = Config(config_str)
extractor = Extractor(config)
extractor.run()
