from extractor.sample.messaging.producer import Producer
from multiprocessing import get_logger

class CalienteUrlProducer(Producer):
    def __init__(self, config):
        """
        Initialize producer instance.
        """
        super().__init__(config)
        self.logger = get_logger()
        self.logger.info(f"initializing {CalienteUrlProducer.__name__} with {config}")

    def send_url(self, url):
        """
        This method calls the inherited produce method to send a new url
        to the configured queue.
        """
        return self.produce(url)