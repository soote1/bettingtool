import time
from extractor.sample.model.Worker import Worker

class OtherSeeder(Worker):
    def do_work(self):
        print("Other seeder here yooo")
        time.sleep(3)