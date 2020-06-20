from multiprocessing import Event, get_logger

class GameMetadata(dict):
    def __init__(self, game_id, game_type, odds, crawled_at):
        self.game_id = game_id
        self.game_type = game_type
        self.odds = odds
        self.crawled_at = crawled_at
