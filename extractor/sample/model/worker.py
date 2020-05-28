class Worker:
    def __init__(self):
        raise NotImplementedError

    def run(self):
        while True:
            self.do_work()
    
    def do_work(self):
        raise NotImplementedError

    def get_state(self):
        raise NotImplementedError

    def update_state(self):
        raise NotImplementedError