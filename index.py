

class Index(object):

    def __init__(self, modules):

        # Store modules ref
        self.modules = modules

    def fetch(self, id):
        data = self.modules.database.get_asset(id)

        return self.modules.factory.parse_database_dict(data)

    def search(self, query):
        pass

    def list_all(self, filter=None):
        results = self.modules.database.query(filter=filter)
        return [value for value in results]
