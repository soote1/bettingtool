class Worker:
    def __init__(self):
        self.name = ""

    def run(self):
        while True:
            self.do_work()
    
    def do_work(self):
        raise NotImplementedError