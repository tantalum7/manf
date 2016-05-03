

class Index(object):

    def __init__(self, app):

        # Store ref to top level app and database
        self._app   = app
        self._db    = app.database

    def fetch(self, id=None, EPN=None):
        pass

    def search(self, query):
        pass

    def list_all(self, filter=None, projection=None):
        pass
