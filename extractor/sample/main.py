from bs4 import BeautifulSoup
import requests

base_href = 'https://sports.caliente.mx'
football_leagues_page = requests.get(f'{base_href}/es_MX/Futbol').text  

soup = BeautifulSoup(football_leagues_page, 'lxml')

league_urls = soup.find('div', {'class':'coupon-builder-for-sport'}).findAll('a')

for league_url in league_urls:
    url = league_url['href']
    name = league_url.text
    print(f'{name}')
    print(f'{base_href}{url}')

    league_matches_page = requests.get(f'{base_href}{url}').text
    soup = BeautifulSoup(league_matches_page, 'lxml')
    matches_table = soup.find_all('tr', {'class':'mkt_content'})
    for match in matches_table:
        full_bets_link = match.find('a', {'title':'Clic aquí para más apuestas'})['href']
        print(full_bets_link)   
        full_bets_page = requests.get(f'{base_href}{full_bets_link}').text
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