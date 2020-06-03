from extractor.sample.messaging.producer import Producer
from multiprocessing import get_logger

class CalienteUrlProducer(Producer):
    def __init__(self, config):
        super().__init__(config)
        self.logger = get_logger()
        self.logger.info(f"initializing {CalienteUrlProducer.__name__} with {self.config}")

    def send_url(self, url):
        self.produce(url)