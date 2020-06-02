from extractor.sample.cache.cache_client import CacheClient

class CalienteSeederCache(CacheClient):
    def __init__(self):
        super().__init__()
        self.leagues = self.client.Array("caliente_seeder_leagues")
        self.matches = self.client.Array("caliente_seeder_matches")
        self.state = self.client.Hash("caliente_seeder_state")

    def update_state(self, new_state):
        self.state.update(state=new_state)
    
    def get_state(self):
        return self.state.get("state").decode("utf-8")
    
    def save_leagues(self, leagues):
        self.leagues = self.client.Array("caliente_leagues")
        self.leagues.clear()
        self.leagues.extend(leagues)

    def get_league(self):
        return self.leagues.pop().decode("utf-8")

    def save_match_odds(self, league, match_odds_list):
        self.matches.extend(match_odds_list)

    def get_match(self):
        return self.matches.pop().decode("utf-8")

    def get_pending_leagues(self):
        return len(self.leagues)

    def clear_lists(self):
        self.update_state("new")
        self.leagues.clear()
        self.matches.clear()