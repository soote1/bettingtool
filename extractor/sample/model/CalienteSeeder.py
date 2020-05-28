from extractor.sample.model.Worker import Worker
import time

class CalienteSeeder(Worker):
    def do_work(self):
        print("Caliente seeder here yooo")
        time.sleep(1)
