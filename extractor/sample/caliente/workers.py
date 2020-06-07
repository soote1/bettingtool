import json
from multiprocessing import get_logger

import requests
from bs4 import BeautifulSoup

from extractor.sample.common.model import Fetcher, Seeder, TimedWorker, Game
from extractor.sample.common.cache import CacheClient
from extractor.sample.common.messaging import Producer, Consumer
from extractor.sample.caliente.model import CalienteSeederConfigKeys, CalienteFetcherConfigKeys, CalienteUrlConsumerConfigKeys, CalienteSeederState
from extractor.sample.caliente.cache import CalienteSeederCache

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

class CalienteOddsProducer(Producer):
    def __init__(self, config):
        """
        Initialize odds producer.
        """
        super().__init__(config)
        self.logger = get_logger()
        self.logger.info(f"initializing {CalienteOddsProducer.__name__} with {config}")

    def send_odds(self, odds):
        """
        This method serializes the odds and calls produce method, 
        which is inherited from base Producer class,
        and passes the serialized odds as argument.
        """
        self.logger.info(f"serializing {odds} to json format")
        serialized_product = json.dumps(odds.__dict__)
        return self.produce(serialized_product)

class CalienteSeeder(Seeder):
    def __init__(self, config):
        """
        Initialize seeder instance.
        """
        super().__init__(config[CalienteSeederConfigKeys.wait_time()])
        self.load_config(config)
        self.logger = get_logger()
        self.cache = CalienteSeederCache(self.cache_config)
        self.current_state = self.get_state()
        self.message_producer = CalienteUrlProducer(self.producer_config)

    def load_config(self, config):
        try:
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
            self.producer_config = config[CalienteSeederConfigKeys.producer_config()]
            self.cache_config = config[CalienteSeederConfigKeys.cache_config()]
        except Exception as error:
            self.logger.error(f"invalid configuration for {CalienteSeeder.__name__}")
            self.logger.error(error)
            raise error


    def do_work(self):
        """
        This method manages the actions that the seeder needs to perform
        depending on the current seeder's state.
        """
        self.current_state = self.get_state()
        self.logger.info(f"{CalienteSeeder.__name__} - {self.current_state}")
        if self.current_state == CalienteSeederState.NEW():
            self.update_state(CalienteSeederState.FETCHING_LEAGUES())
            self.get_leagues()
        elif self.current_state == CalienteSeederState.FETCHING_LEAGUES():
            self.get_leagues()
        elif self.current_state == CalienteSeederState.FETCHING_MATCHES():
            if self.cache.get_pending_leagues() == 0:
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
        try:
            football_leagues_page = requests.get(self.leagues_url).text
        except Exception as error:
            self.logger.error("problems found while making the http request... waiting for next attempt")
            self.logger.error(error)
            return

        try:
            soup = BeautifulSoup(football_leagues_page, self.html_parser)
            league_urls_container = soup.find(self.leagues_container_type, self.leagues_container_target)
            league_url_elements = league_urls_container.findAll(self.league_url_type)
            league_urls = []
            for league_url_element in league_url_elements:
                url = league_url_element[self.league_url_target]
                name = league_url_element.text
                league_urls.append(f"{self.base_href}{url}")
                self.logger.info(f"league name: {name} url: {url}")
        except Exception as error:
            self.logger.error(f"problems found while trying to extract the data from the dom... waiting for next attempt")
            self.logger.error(error)
            return

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
            self.logger.info("no soccer match url available, updating seeder state and waiting for next attempt")
            self.set_seeder_ready()
            return

        try:
            league_matches_page = requests.get(url).text
        except Exception as error:
            self.logger.error("problems found while making the http request... waiting for next attempt")
            self.logger.error(error)
            return

        try:
            self.logger.info(f"fetching odds for all matches in league {url}")
            soup = BeautifulSoup(league_matches_page, self.html_parser)
            matches_table = soup.find_all(self.matches_container_type, self.matches_container_target)
            match_odds_list = []
            for match in matches_table:
                full_bets_link = match.find(self.odds_container_type, self.odds_container_target)[self.odds_link_target]
                match_odds_list.append(f"{self.base_href}{full_bets_link}")
                self.logger.info(f"bets page link: {full_bets_link}")
        except Exception as error:
            self.logger.error(f"problems found while trying to extract the data from the dom object... waiting for next attempt")
            self.logger.error(error)
            return

        self.save_match_odds_urls(match_odds_list)

    def save_match_odds_urls(self, match_odds_urls):
        self.logger.info("saving odds' links in cache server")
        self.cache.save_match_odds(match_odds_urls)

    def get_match_url(self):
        self.logger.info("fetching odds link from cache")
        return self.cache.get_match()

    def send_odds_link(self):
        """
        Retrieves an url from the cache and tells the producer to
        send the url to the corresponding queue so that it can be used
        by a fetcher instance.
        """
        match_url = self.get_match_url()
        return self.message_producer.send_url(match_url)

class CalienteUrlConsumer(Consumer):
    def __init__(self, config):
        """
        Initialize consumer instance.
        """
        self.logger = get_logger()
        super().__init__(CalienteUrlConsumer.__name__, config)
        self.load_config(config)
        self.odds_fetcher = CalienteFetcher(self.fetcher_config)
        self.odds_producer = CalienteOddsProducer(self.producer_config)

    def load_config(self, config):
        """
        Loads config values from dictionary
        """
        try:
            self.logger.info(f"initializing {CalienteUrlConsumer.__name__} with {config}")
            self.producer_config = config[CalienteUrlConsumerConfigKeys.producer_config()]
            self.fetcher_config = config[CalienteUrlConsumerConfigKeys.fetcher_config()]
            self.decode_format = config[CalienteUrlConsumerConfigKeys.decode_format()]
        except Exception as error:
            self.logger.error(f"invalid configuration for {CalienteUrlConsumer.__name__}")
            self.logger.error(error)
            raise error

    def do_work(self, ch, method, properties, body):
        """
        This method is called when a message is received in the configured queue.
        It tells the fetcher to process the url and waits for the result. If the
        result isn't None, then it calls the send_odds method and passes the fetcher's
        result as argument.
        """
        self.logger.info(f"received new message with body => {body}")
        odds = self.get_odds_from_fetcher(body.decode(self.decode_format))

        if odds == None:
            self.logger.info(f"no odds found for {body}")
        else:            
            odds_sent = self.send_odds(odds)
            if odds_sent:
                self.logger.info("message sent... removing from queue")
            else:
                self.logger.info("the message couldn't be delivered to the queue... keeping in it for next attempt")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def get_odds_from_fetcher(self, url):
        """
        Tells the fetcher to retrieve the odds for a given url
        """
        self.logger.info("passing url to fetcher and waiting for the odds")
        return self.odds_fetcher.fetch(url)


    def send_odds(self, odds):
        """
        Tells the producer to send a serialized version of the odds to the configured queue.
        """
        self.logger.info("passing the odds to the producer")
        return self.odds_producer.send_odds(odds)

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

class CalienteCacheCleaner(TimedWorker):
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
