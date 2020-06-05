class ConfigKeys(object):
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

    @staticmethod
    def worker_module():
        return 0
    
    @staticmethod
    def worker_class():
        return 1
    
    @staticmethod 
    def worker_config():
        return 2