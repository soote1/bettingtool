from extractor.sample.model.worker import Worker

class Seeder(Worker):
    def __init__(self, name, wait_time):
        super().__init__(name, wait_time)
