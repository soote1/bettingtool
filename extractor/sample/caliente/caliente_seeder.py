import requests
from bs4 import BeautifulSoup
from extractor.sample.workers.seeder import Seeder
from extractor.sample.caliente.caliente_seeder_config_keys import CalienteSeederConfigKeys
from extractor.sample.caliente.caliente_seeder_cache import CalienteSeederCache
from extractor.sample.caliente.caliente_url_producer import CalienteUrlProducer

class CalienteSeeder(Seeder):
    def __init__(self, config):
        self.config = config
        super().__init__(CalienteSeeder.__name__, self.config[CalienteSeederConfigKeys.WAIT_TIME()])
        self.logger.info(f"intializing {CalienteSeeder.__name__} with {self.config}")
        self.cache = CalienteSeederCache()
        self.current_state = self.get_state()
        self.producer_config = self.config[CalienteSeederConfigKeys.PRODUCER_CONFIG()]
        self.message_producer = CalienteUrlProducer(self.producer_config)

    def do_work(self):
        self.current_state = self.get_state()
        self.logger.info(f"{self.name} - {self.current_state}")
        if self.current_state == "new":
            self.update_state("fetching_leagues")
            self.get_leagues()
        elif self.current_state == "fetching_matches":
            if(self.cache.get_pending_leagues() == 0):
                self.set_seeder_ready()
            else:
                self.get_matches()
        elif self.current_state== "ready":
            self.send_odds_link()

    def get_state(self):
        state = self.cache.get_state()
        return "new" if self.cache.get_state() == None else state

    def update_state(self, new_state):
        self.current_state = new_state
        self.cache.update_state(self.current_state)

    def set_seeder_ready(self):
        self.logger.info("seeder is ready, updating state...")
        self.update_state("ready")
        self.cache.update_state(self.current_state)

    def get_leagues(self):
        """
        Get all leagues' URLs
        """
        self.logger.info("fetching leagues' URLs")
        football_leagues_page = requests.get(f"{self.config['base_href']}/es_MX/Futbol").text  
        soup = BeautifulSoup(football_leagues_page, "lxml")
        league_url_elements = soup.find("div", {'class':'coupon-builder-for-sport'}).findAll("a")
        league_urls = []
        for league_url_element in league_url_elements:
            url = league_url_element["href"]
            name = league_url_element.text
            league_urls.append(f"{self.config['base_href']}{url}")
            self.logger.info(f"league name: {name} url: {url}")

        self.logger.info(f"saving leagues' URLs")
        self.cache.save_leagues(league_urls)
        self.update_state("fetching_matches")

    def get_matches(self):
        """
        Get all matches' URLs per each league
        """
        url = self.cache.get_league()
        self.logger.info(f"fetching odds for all matches in league {url}")
        league_matches_page = requests.get(url).text
        soup = BeautifulSoup(league_matches_page, 'lxml')
        matches_table = soup.find_all("tr", {"class":"mkt_content"})
        match_odds_list = []
        for match in matches_table:
            full_bets_link = match.find("a", {"title":"Clic aquí para más apuestas"})["href"]
            match_odds_list.append(f"{self.config['base_href']}{full_bets_link}")
            self.logger.info(f"bets page link: {full_bets_link}")
        self.logger.info("saving odds' links")
        self.cache.save_match_odds(url, match_odds_list)

    def send_odds_link(self):
        self.logger.info("fetching odds link from cache")
        match_odds_url = self.cache.get_match()
        self.logger.info(f"sending {match_odds_url}")
        self.message_producer.send_url(match_odds_url)