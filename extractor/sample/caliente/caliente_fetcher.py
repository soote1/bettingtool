import requests
from bs4 import BeautifulSoup
from multiprocessing import get_logger

from extractor.sample.workers.fetcher import Fetcher
from extractor.sample.model.game import Game
from extractor.sample.caliente.caliente_fetcher_config_keys import CalienteFetcherConfigKeys

class CalienteFetcher(Fetcher):
    def __init__(self, config):
        """
        Initialize fetcher's instance.
        """
        self.name = CalienteFetcher.__name__
        self.logger = get_logger()
        self.load_config(config)

    def load_config(self, config):
        try:
            self.logger.info(f"intializing {CalienteFetcher.__name__} with {config}")
            self.parser = config[CalienteFetcherConfigKeys.parser()]
            self.correct_score_game_container_type = config[CalienteFetcherConfigKeys.correct_score_game_container_type()]
            self.correct_score_game_container_target = config[CalienteFetcherConfigKeys.correct_score_game_container_target()]
            self.odds_container_type = config[CalienteFetcherConfigKeys.odds_container_type()]
            self.odds_container_target = config[CalienteFetcherConfigKeys.odds_container_target()]
            self.odd_label_target = config[CalienteFetcherConfigKeys.odd_label_target()]
            self.odd_value_container_type = config[CalienteFetcherConfigKeys.odd_value_container_type()]
            self.odd_value_container_taget = config[CalienteFetcherConfigKeys.odd_value_container_target()]
            self.game_type = config[CalienteFetcherConfigKeys.game_type()]
        except Exception as error:
            self.logger.error(f"invalid configuration for {CalienteFetcher.__name__} class")
            self.logger.error(error)
            raise error

    def fetch(self, url):
        """
        This method retrieves the content from a given url and returns
        the result from parse_results method.
        """
        try:
            self.logger.info(f"{self.name} - fetching odds page from {url}")
            odds_page = requests.get(url).text
        except Exception as error:
            self.logger.error(f"problems found while trying to get the data from {url} ... waiting for next attempt")
            self.logger.error(error)
            return None

        return self.parse_results(url, odds_page)
        

    def parse_results(self, url, odds_page):
        """
        This method creates a beautifulsoup object to parse the content received as argument
        and extracts the odds for a specific type of bet. It returns a Game object, which
        includes the list of odds found and related metadata. It returns None if there is an 
        error while trying to extract the data from the beautifulsoup object.
        """
        try:
            self.logger.info(f"{self.name} - parsing results")
            soup = BeautifulSoup(odds_page, self.parser)
            correct_score_table = soup.find(self.correct_score_game_container_type, self.correct_score_game_container_target)
            odds_container = correct_score_table.find_all(self.odds_container_type, self.odds_container_target)
            odds = []
            for odd in odds_container:
                odd_values = [odd[self.odd_label_target], odd.find(self.odd_value_container_type, self.odd_value_container_taget).text]
                odds.append(odd_values)
            return Game(url, self.game_type, odds)
        except Exception as error:
            self.logger.error(f"{self.name} error found while trying to extract the data from the html tree {error}")    
            return None
