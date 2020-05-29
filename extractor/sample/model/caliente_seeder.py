import time
from extractor.sample.model.seeder import Seeder

class CalienteSeeder(Seeder):
    def __init__(self, wait_time):
        self.wait_time = wait_time
        self.name = "caliente_seeder"

    def do_work(self):
        print(f"{self.name} here yooo")

    def get_leagues_urls(self):
        """
        Get all leagues' URLs
        """
        pass

    def get_matches_per_league_urls(self):
        """
        Get all matches' URLs per each league
        """
        pass