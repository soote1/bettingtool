import os

from extractor.sample.manager import Extractor, ConfigHelper

extractor = Extractor(f"{os.path.dirname(__file__)}/config.json")
extractor.run()
