import requests
from bs4 import BeautifulSoup
from multiprocessing import get_logger
from extractor.sample.workers.seeder import Seeder
from extractor.sample.caliente.caliente_seeder_config_keys import CalienteSeederConfigKeys
from extractor.sample.caliente.caliente_seeder_cache import CalienteSeederCache
from extractor.sample.caliente.caliente_url_producer import CalienteUrlProducer
from extractor.sample.caliente.caliente_seeder_state import CalienteSeederState

class CalienteSeeder(Seeder):
    def __init__(self, config):
        """
        Initialize seeder instance.
        """
        self.logger = get_logger()
        self.load_config(config)
        super().__init__(CalienteSeeder.__name__, self.wait_time)
        self.cache = CalienteSeederCache(self.cache_config)
        self.current_state = self.get_state()
        self.message_producer = CalienteUrlProducer(self.producer_config)

    def load_config(self, config):
        self.logger.info(f"intializing {CalienteSeeder.__name__} with {config}")
        self.base_href = config[CalienteSeederConfigKeys.base_href()]
        self.leagues_url = f"{self.base_href}{config[CalienteSeederConfigKeys.leagues_path()]}"
        self.leagues_container_type = config[CalienteSeederConfigKeys.leagues_container_type()]
        self.leagues_container_target = config[CalienteSeederConfigKeys.leagues_container_target()]
        self.league_url_type = config[CalienteSeederConfigKeys.league_url_type()]
        self.league_url_target = config[CalienteSeederConfigKeys.league_url_target()]
        self.matches_container_type = config[CalienteSeederConfigKeys.matches_container_type()]
        self.matches_container_target = config[CalienteSeederConfigKeys.matches_container_target()]
        self.odds_container_type = config[CalienteSeederConfigKeys.odds_container_type()]
        self.odds_container_target = config[CalienteSeederConfigKeys.odds_container_target()]
        self.odds_link_target = config[CalienteSeederConfigKeys.odds_link_target()]
        self.html_parser = config[CalienteSeederConfigKeys.html_parser()]
        self.wait_time = config[CalienteSeederConfigKeys.wait_time()]
        self.producer_config = config[CalienteSeederConfigKeys.producer_config()]
        self.cache_config = config[CalienteSeederConfigKeys.cache_config()]

    def do_work(self):
        """
        This method manages the actions that the seeder needs to perform
        depending on the current seeder's state.
        """
        self.current_state = self.get_state()
        self.logger.info(f"{self.name} - {self.current_state}")
        if self.current_state == CalienteSeederState.NEW():
            self.update_state(CalienteSeederState.FETCHING_LEAGUES())
            self.get_leagues()
        elif self.current_state == CalienteSeederState.FETCHING_MATCHES():
            if(self.cache.get_pending_leagues() == 0):
                self.set_seeder_ready()
            else:
                self.get_matches()
        elif self.current_state== CalienteSeederState.READY():
            self.send_odds_link()

    def get_state(self):
        """
        Retrieves the seeder's state from the cache server. 
        Returns None if state hasn't been set.
        """
        state = self.cache.get_state()
        return CalienteSeederState.NEW() if state == None else state

    def update_state(self, new_state):
        """
        Tells the cache client to update the current seeder's state.
        """
        self.current_state = new_state
        self.cache.update_state(self.current_state)

    def set_seeder_ready(self):
        """
        Tells the cache client to set the current seeder's state as 'ready'.
        """
        self.logger.info("seeder is ready, updating state...")
        self.update_state(CalienteSeederState.READY())

    def get_leagues(self):
        """
        Retrieves the content of the page containing all the soccer leagues urls,
        then creates a beautifulsoup object to parse the result and extract the urls
        from the dom. Finally, tells the cache client to store the urls in the cache server
        and updates the current seeder's state.
        """
        self.logger.info(f"fetching leagues' URLs from {self.leagues_url}")
        football_leagues_page = requests.get(self.leagues_url).text
        soup = BeautifulSoup(football_leagues_page, self.html_parser)
        league_url_elements = soup.find(self.leagues_container_type, self.leagues_container_target).findAll(self.league_url_type)
        league_urls = []
        for league_url_element in league_url_elements:
            url = league_url_element[self.league_url_target]
            name = league_url_element.text
            league_urls.append(f"{self.base_href}{url}")
            self.logger.info(f"league name: {name} url: {url}")

        self.logger.info(f"saving leagues' URLs")
        self.cache.save_leagues(league_urls)
        self.update_state(CalienteSeederState.FETCHING_MATCHES())

    def get_matches(self):
        """
        Retrieves the content of the page containing all the urls for all the soccer mathces
        for a given league, then creates a beautifulsoup object to parse the result and extract 
        from the dom the odds urls for each match. Finally, tells the cache client to store the 
        urls in the cache server and updates the current seeder's state.
        """
        url = self.cache.get_league()
        if url == None:
            self.set_seeder_ready()
            return

        self.logger.info(f"fetching odds for all matches in league {url}")
        league_matches_page = requests.get(url).text
        soup = BeautifulSoup(league_matches_page, self.html_parser)
        matches_table = soup.find_all(self.matches_container_type, self.matches_container_target)
        match_odds_list = []
        for match in matches_table:
            full_bets_link = match.find(self.odds_container_type, self.odds_container_target)[self.odds_link_target]
            match_odds_list.append(f"{self.base_href}{full_bets_link}")
            self.logger.info(f"bets page link: {full_bets_link}")
        self.logger.info("saving odds' links")
        self.cache.save_match_odds(url, match_odds_list)

    def send_odds_link(self):
        """
        Retrieves an url from the cache and tells the producer to
        send the url to the corresponding queue so that it can be used
        by a fetcher instance.
        """
        self.logger.info("fetching odds link from cache")
        match_odds_url = self.cache.get_match()
        self.logger.info(f"sending {match_odds_url}")
        self.message_producer.send_url(match_odds_url)