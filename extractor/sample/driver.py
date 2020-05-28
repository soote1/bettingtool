from multiprocessing import Process
from extractor.sample.model.other_seeder import OtherSeeder
from extractor.sample.model.caliente_seeder import CalienteSeeder

processes = []
worker_types = (CalienteSeeder, OtherSeeder)

# create processes
for worker_type in worker_types:
    worker_instance = worker_type()
    processes.append(Process(target=worker_instance.run))

# start all processes
for process in processes:
    process.start()