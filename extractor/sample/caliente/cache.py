import datetime
from multiprocessing import get_logger

from walrus import Model, DateTimeField, TextField

from extractor.sample.common.cache import CacheClient, BaseModel

class Worker(BaseModel):
    name = TextField(primary_key=True)
    state = TextField(index=True)

class League(BaseModel):
    url = TextField(primary_key=True)

class Game(BaseModel):
    url = TextField(primary_key=True)
    last_crawl = DateTimeField(index=True)

class CalienteSeederCache(CacheClient):
    def __init__(self, config):
        """
        Initialize wrapper.
        """
        super().__init__(config)
        self.logger = get_logger()

    def create_worker_state(self, name, state):
        self.logger.info(f"Creating worker state with name={name} state={state}")
        Worker.__database__ = self.client
        Worker.create(name=name, state=state)

    def get_worker_state(self, name):
        """
        Fetchs worker state from cache server
        """
        # TODO: handle KeyError when worker state doesn't exist
        try:
            self.logger.info("fetching worker state from cache")
            return Worker.load(name).state
        except KeyError as error:
            self.logger.info("worker state not initialized")
            return None

    def update_worker_state(self, name, new_state):
        """
        Updates seeder's state in the cache server.
        """
        self.logger.info("updating worker state")
        try:
            worker_state = Worker.load(name)
            worker_state.state = new_state
            worker_state.save()
        except KeyError as error:
            self.logger.info("worker state not initialized... creating new instance")
            self.create_worker_state(name, new_state)
    
    def save_leagues(self, leagues):
        """
        Saves a list of league URLs.
        """
        for league in leagues:
            self.save_league(league)

    def save_league(self, league):
        """
        Saves new league url in the cache server.
        """
        self.logger.info(f"saving {league} in cache server")
        League.__database__ = self.client
        League.create(url=league)

    def get_league(self):
        """
        Retrieves a random league url from the cache server.
        """
        self.logger.info("fetching league url from cache server")
        league = next(League.all())
        league.delete()
        return league.url

    def save_games(self, games_urls, crawled_at):
        """
        Saves the urls for all the matches on a given league in the cache server.
        """
        for game_url in games_urls:
            self.save_game(game_url, crawled_at)
    
    def save_game(self, match_url, last_crawl):
        self.logger.info(f"saving new game with url={match_url} processing_count={last_crawl}")
        Game.__database__ = self.client
        Game.create(url=match_url, last_crawl=last_crawl)

    def get_oldest_game_url(self):
        """
        Returns the oldest game url.
        """
        self.logger.info("fetching oldest game url from cache server")
        for game in Game.query(order_by=Game.last_crawl):
            game.last_crawl = datetime.datetime.utcnow()
            game.save()
            return game.url

        return None

    def get_pending_leagues(self):
        """
        Retrieves the current count of URLs which are available in the cache server.
        """
        return League.count()