

from database   import Database
from asset      import Asset

class Manf(object):

    class _Modules(object):
        database = None

    def __init__(self):

        # Init modules
        self.modules = self._Modules()
        self.modules.database = Database()




if __name__ == "__main__":


    manf = Manf()

    a1 = manf.modules.database.create_asset({"toast" : 6})
    a2 = manf.modules.database.create_asset({"toast" : 7})
    a3 = manf.modules.database.create_asset({"toast" : 8})
    a4 = manf.modules.database.create_asset({"toast" : 9})

    result = manf.modules.database.query( {'toast' : {'$lt' : 8} } )

    print result
    pass