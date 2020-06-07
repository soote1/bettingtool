from multiprocessing import get_logger

from extractor.sample.cache.cache_client import CacheClient
from extractor.sample.workers.timed_worker import TimedWorker

class CacheCleaner(TimedWorker):
    def __init__(self, config):
        """
        Initialize cache cleaner instance
        """
        super().__init__(config["wait_time"])
        self.logger = get_logger()
        self.cache_client = CacheClient()

    def do_work(self):
        """
        Tells the cache client to flush all the keys in the server
        """
        self.logger.info("flushing all keys in cache server")
        self.cache_client.clean_cache()