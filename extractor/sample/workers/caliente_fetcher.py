import requests
from bs4 import BeautifulSoup
from multiprocessing import get_logger

from extractor.sample.workers.fetcher import Fetcher
from extractor.sample.model.game import Game

class CalienteFetcher(Fetcher):
    def __init__(self):
        self.name = CalienteFetcher.__name__
        self.logger = get_logger()
        self.logger.info(f"{self.name} - initialized")

    def fetch(self, url):
        self.logger.info(f"{self.name} - fetching odds page from {url}")
        odds_page = requests.get(url).text
        return self.parse_results(url, odds_page)
        

    def parse_results(self, url, odds_page):
        self.logger.info(f"{self.name} - parsing results")
        soup = BeautifulSoup(odds_page, "lxml")
        try:
            correct_score_table = soup.find("table", {"class":"correct-score"})
            odds_container = correct_score_table.find_all("button", {"class":"price"})
            odds = []
            for odd in odds_container:
                odd_values = [odd["title"], odd.find("span", {"class":"price us"}).text]
                odds.append(odd_values)
            return Game(url, "correct_score", odds)
        except Exception as error:
            self.logger.error(f"{self.name} error found while trying to extract the data from the html tree {error}")    
            return None
