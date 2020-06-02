import requests
from bs4 import BeautifulSoup
from extractor.sample.workers.fetcher import Fetcher

class CalienteFetcher(Fetcher):
    def __init__(self):
        self.base_href ="" #TODO: read this from config file
        self.full_bets_link = "" #TODO: get url from queue


    def fetch(self):
        full_bets_page = requests.get(f'{self.base_href}{self.full_bets_link}').text
        soup = BeautifulSoup(full_bets_page, 'lxml')
        try:
            correct_score_table = soup.find('table', {'class':'correct-score'})
            odds = correct_score_table.find_all('button', {'class':'price'})

            for odd in odds:
                score = odd['title']
                odd_value = odd.find('span', {'class':'price us'}).text
                print(f'{score} {odd_value}')
        except:    
            print('no matches found')
