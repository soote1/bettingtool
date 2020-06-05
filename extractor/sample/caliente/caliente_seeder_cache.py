from extractor.sample.cache.cache_client import CacheClient
from extractor.sample.caliente.caliente_cache_keys import CalienteCacheKeys

from multiprocessing import get_logger

class CalienteSeederCache(CacheClient):
    def __init__(self, config):
        """
        Initialize wrapper.
        """
        super().__init__()
        self.logger = get_logger()
        self.load_config(config)
        self.load_keys()

    def load_config(self, config):
        self.logger.info(f"initializing {CalienteSeederCache.__name__} with {config}")
        self.leagues_key = config[CalienteCacheKeys.leagues_key()]
        self.matches_key = config[CalienteCacheKeys.matches_key()]
        self.state_key = config[CalienteCacheKeys.state_key()]
        self.state_value_key = config[CalienteCacheKeys.state_value_key()]
        self.initial_state = config[CalienteCacheKeys.initial_state()]
        self.decode_format = config[CalienteCacheKeys.decode_format()]

    def load_keys(self):
        self.leagues = self.client.Array(self.leagues_key)
        self.matches = self.client.Array(self.matches_key)
        self.state = self.client.Hash(self.state_key)

    def update_state(self, new_state):
        """
        Updates seeder's state in the cache server.
        """
        self.state[self.state_value_key] = new_state
    
    def get_state(self):
        """
        Retrieves seeder's state from the cache server.
        """
        state = self.state.get(self.state_value_key)
        return state.decode(self.decode_format) if not state == None else state
    
    def save_leagues(self, leagues):
        """
        Saves the urls for all the leagues in the cache server.
        """
        self.leagues.clear()
        self.leagues.extend(leagues)

    def get_league(self):
        """
        Retrieves a random league url from the cache server.
        """
        return self.leagues.pop().decode(self.decode_format)

    def save_match_odds(self, league, match_odds_list):
        """
        Saves the urls for all the matches on a given league in the cache server.
        """
        self.matches.extend(match_odds_list)

    def get_match(self):
        """
        Retrieves a random match url from the cache server.
        """
        return self.matches.pop().decode(self.decode_format)

    def get_pending_leagues(self):
        """
        Retrieves the current count of URLs which are available in the cache server.
        """
        return len(self.leagues)