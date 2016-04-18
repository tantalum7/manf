
# Library imports


# Project imports
from database       import Database
from factory        import Factory
from index          import Index
from settings       import Settings


class Modules(object):
    database    = None
    factory     = None
    server      = None
    settings    = None
    index       = None


class Manf(object):

    def __init__(self):

        # Init modules
        self.modules            = Modules()
        self.modules.database   = Database(self.modules)
        self.modules.factory    = Factory(self.modules)
        self.modules.index      = Index(self.modules)
        self.modules.settings   = Settings()




if __name__ == "__main__":

    mani = Manf()

    r = mani.modules.index.fetch("200")

    all = mani.modules.index.list_all({"_type" : "*PART"})

    print "Done"