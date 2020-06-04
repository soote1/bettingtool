class Game(dict):
    def __init__(self, game_id, game_type, odds):
        self.game_id = game_id
        self.game_type = game_type
        self.odds = odds