
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


    # for x in range(10):
    #
    #     part = mani.modules.factory.create_part()
    #
    #     part.EPN            = "R_"+str(x * 10)+"K_0402"
    #     part.description    = "SMD chip resistor"
    #     part.component_type = "RESISTOR_SMD"
    #     part.manufacturer   = "ROHM"
    #     part.MPN            = "12345678"


    all = mani.modules.index.list_all({"_type": "*PART"})
    print "Number of items "+str(len(all))
    for a in all:
        #print a['@part']['EPN']
        part = mani.modules.index.fetch(a['_id'])
        print part.EPN, part.description

        pass

    print "Done"