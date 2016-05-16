

class Settings(object):

    def __init__(self):
        self.db_find_modifiers = {"$maxTimeMS" : 500}
        self.request_time_warning   = 1000 #msec