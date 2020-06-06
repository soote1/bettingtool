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
        Loads configuration from dictionary
        """
        try:
            self.logger.info(f"loading {CacheCleaner.__name__} with {config}")
            self.wait_time = config["wait_time"]
        except Exception as error:
            self.logger.error(f"invalid configuration for {CacheCleaner.__name__} class")
            self.logger.error(error)
            raise error

    def do_work(self):
        """
        Tells the cache client to flush all the keys in the server
        """
        self.logger.info("flushing all keys in cache server")
        self.cache_client.clean_cache()