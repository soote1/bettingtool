class CalienteUrlConsumerConfigKeys:
    @staticmethod
    def producer_config():
        return "producer_config"

    @staticmethod
    def fetcher_config():
        return "fetcher_config"

    @staticmethod
    def decode_format():
        return "decode_format"

class CalienteSeederState:
    @staticmethod
    def NEW():
        return "new"
    @staticmethod
    def FETCHING_LEAGUES():
        return "fetching_leagues"
    @staticmethod
    def FETCHING_MATCHES():
        return "fetching_matches"
    @staticmethod
    def READY():
        return "ready"

class CalienteSeederConfigKeys(object):
    @staticmethod
    def wait_time():
        return "wait_time"
    
    @staticmethod
    def base_href():
        return "base_href"

    @staticmethod
    def producer_config():
        return "producer_config"

    @staticmethod
    def leagues_path():
        return "leagues_path"

    @staticmethod
    def html_parser():
        return "html_parser"

    @staticmethod
    def leagues_container_type():
        return "leagues_container_type"
    
    @staticmethod 
    def leagues_container_target():
        return "leagues_container_target"

    @staticmethod
    def league_url_type():
        return "league_url_type"
    
    @staticmethod
    def league_url_target():
        return "league_url_target"
    
    @staticmethod
    def matches_container_type():
        return "matches_container_type"

    @staticmethod
    def matches_container_target():
        return "matches_container_target"
    
    @staticmethod
    def odds_container_target():
        return "odds_container_target"

    @staticmethod
    def odds_container_type():
        return "odds_container_type"

    @staticmethod
    def odds_link_target():
        return "odds_link_target"

    @staticmethod
    def cache_config():
        return "cache_config"

class CalienteFetcherConfigKeys:
    @staticmethod
    def parser():
        return "parser"

    @staticmethod
    def correct_score_game_container_type():
        return "correct_score_game_container_type"

    @staticmethod
    def correct_score_game_container_target():
        return "correct_score_game_container_target"

    @staticmethod
    def odds_container_type():
        return "odds_container_type"
    
    @staticmethod
    def odds_container_target():
        return "odds_container_target"

    @staticmethod
    def odd_label_target():
        return "odd_label_target"

    @staticmethod
    def odd_value_container_type():
        return "odd_value_container_type"

    @staticmethod
    def odd_value_container_target():
        return "odd_value_container_target"
    
    @staticmethod
    def game_type():
        return "game_type"
