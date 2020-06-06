from multiprocessing import get_logger
from extractor.sample.cache.cache_client import CacheClient
from extractor.sample.workers.worker import Worker

class CacheCleaner(Worker):
    def __init__(self, config):
        """
        Initialize cache cleaner instance
        """
        self.logger = get_logger()
        self.load_config(config)
        super().__init__(CacheCleaner.__name__, self.wait_time)
        self.cache_client = CacheClient()

    def load_config(self, config):
        """
        loads configuration from dictionary
        """
        self.wait_time = config["wait_time"]

    def do_work(self):
        """
        tells the cache client to flush all the keys in the server
        """
        self.logger.info("flushing all keys in cache server")
        self.cache_client.clean_cache()