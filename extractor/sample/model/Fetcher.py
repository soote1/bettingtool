from bs4 import BeautifulSoup
import requests

class Fetcher:
    def __init__(self):
        self.base_href = 'https://sports.caliente.mx'

    def fetch(self):
        football_leagues_page = requests.get(f'{self.base_href}/es_MX/Futbol').text  
        soup = BeautifulSoup(football_leagues_page, 'lxml')
        league_urls = soup.find('div', {'class':'coupon-builder-for-sport'}).findAll('a')

        for league_url in league_urls:
            url = league_url['href']
            name = league_url.text

            league_matches_page = requests.get(f'{self.base_href}{url}').text
            soup = BeautifulSoup(league_matches_page, 'lxml')
            matches_table = soup.find_all('tr', {'class':'mkt_content'})
            for match in matches_table:
                full_bets_link = match.find('a', {'title':'Clic aquí para más apuestas'})['href']
                print(full_bets_link)
    
    def get_fetcher_state(self):
        pass

    def update_fetcher_state(self):
        pass