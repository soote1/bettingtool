import time
from extractor.sample.model.seeder import Seeder

class OtherSeeder(Seeder):
    def __init__(self, wait_time):
        self.name = "other_seeder"
        self.wait_time = wait_time

    def do_work(self):
        print(f"{self.name} here yooo")