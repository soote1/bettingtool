class ExtractorConfigKeys(object):
    @staticmethod
    def producers():
        return "producers"
    
    @staticmethod
    def consumers():
        return "consumers"
    
    @staticmethod
    def seeders():
        return "seeders"
    
    @staticmethod
    def fetchers():
        return "fetchers"
    
    @staticmethod
    def listeners():
        return "listeners"
    
    @staticmethod
    def wait_time():
        return "wait_time"