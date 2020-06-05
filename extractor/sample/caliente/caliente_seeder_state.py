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
    