import time
from extractor.sample.model.seeder import Seeder

class OtherSeeder(Seeder):
    def __init__(self):
        self.name = "other_seeder"

    def do_work(self):
        print(f"{self.name} here yooo")
        time.sleep(3)