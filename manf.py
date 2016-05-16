
# Library imports


# Project imports
from constants       import Constants
from database       import Database
from factory        import Factory
from google_auth    import GoogleAuth
from index          import Index
from settings       import Settings
from google_auth    import GoogleAuth
from constants       import Constants


class Manf(object):

    class NotFoundError(Exception):
        pass

    def __init__(self, db_addr=("45.58.35.135", 27027)):

        # Init class vars
        self.database   = Database( ("45.58.35.135", 27027) )
        self.factory    = Factory(self)
        self.index      = Index(self)
        self.settings   = Settings()
        self.auth       = GoogleAuth("client_secrets.json")
        self.constants  = Constants(self)

        pass



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


    #bom = mani.modules.factory.create_build_standard()

    bom = mani.factory.create_build_standard()

    bom.name        = "ANOTHER_TEST_BOM"
    bom.revision    = "4.2"

    csv_str = """Reference, Value, Footprint,EPN
    U1,XC9103,TO_SOT_Packages_SMD:SOT-23-5,XC9103_SOT23-5
    D1,MBR230LSFT1G,Diodes_SMD:SOD-123,MBR230LSFT1G_SOD123
    L1,10u,dong:5X5X4_BOURNS_INDUCTOR,IND_10U_2A_5X5
    R1,3K3,Resistors_SMD:R_0402,R_3K3_0402
    R3,10K,Resistors_SMD:R_0402,R_10K_0402
    R2,10K,Resistors_SMD:R_0402,R_10K_0402"""

    bom.process_csv(csv_str)

    print "Done"