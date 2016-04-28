
# Library imports
import csv

# Project imports
from asset      import Asset, AssetType
from util_funcs import recursive_dict_update

def _CsvReaderHelper(csv_data):

    class _dialect(csv.Dialect):
        def __init__(self):

            self.skipinitialspace   = True
            self.delimiter          = ','
            self.quotechar          = '|'
            self.quoting            = csv.QUOTE_MINIMAL
            self.lineterminator     = "\r\n"
            csv.Dialect.__init__(self)

    return csv.reader(csv_data, dialect=_dialect())

class BuildStandard(Asset):

    CSV_COL_REF         = ["REF", "Reference", "REFERENCE", "Ref"]
    CSV_COL_VALUE       = ["VAL", "Value", "VALUE", "Val"]
    CSV_COL_FOOTPRINT   = ["FP", "Footprint", "FOOTPRINT"]
    CSV_COL_EPN         = ["EPN", "epn", "Engineering Part Number"]
    CSV_COL_DNF         = ["DNF", "dnf", "DO NOT FIT", "Do not fit"]

    def __init__(self, db, id=None, fields=None):
        pass
        # Commented out all the DB stuff so its purely a local temporary object
        # # Define default fields dict
        # default = { '_type'          : AssetType.BUILD_STANDARD,
        #             '@history'       : {},
        #             '@data'          : {},
        #             '@bom'           : { 'NAME'         : '',
        #                                  'STATUS'       : '',
        #                                  'DESCRIPTION'  : '',
        #                                  'REVISION'     : '',
        #                                  'APPROVAL'     : '',
        #                                  'BOM_TYPE'     : '',
        #                               },
        #          }
        #
        # # If a fields dict was passed, update the default dict with it
        # if fields:
        #     default = recursive_dict_update(default, fields)
        #
        # # Init parent class
        # Asset.__init__(self, db, fields=default, id=id)

    def process_csv(self, csv_string):

        # Create csv reader
        csv_reader = _CsvReaderHelper(csv_string.splitlines())

        # Grab the first line which should be the column headings
        columns = csv_reader.next()

        # Prepare list of column headings we are looking for (list of list of spelling variants)
        col_headings_list = [ self.CSV_COL_REF, self.CSV_COL_VALUE, self.CSV_COL_EPN,
                              self.CSV_COL_FOOTPRINT, self.CSV_COL_DNF ]

        # Prepare dict to store the index location of the headings
        col_index_dict = {}

        # Iterate through the column headings list
        for col_heading_spelling_list in col_headings_list:

            # Create var to store first spelling variant to act as key in the dict
            col_name = col_heading_spelling_list[0]

            # Iterate through the various acceptable spellings of column heading
            for text in col_heading_spelling_list:

                # Try and find an instance of the ref string in the columns
                try:
                    i = columns.index(text)

                # Ignore value error raised by not finding the string
                except ValueError:
                    pass

                # Raise any other exceptions higher
                except:
                    raise

                # If we found the string instance, stick the index in the dict then break out the loop
                else:
                    col_index_dict[col_name] = i
                    continue

        # Prepare empty bom list
        bom = []

        # Iterate through the rest of the csv
        for line in csv_reader:

            # Create a dict to store bom item's data
            d = { 'REF'     : col_index_dict['REF'],
                  'VALUE'   : col_index_dict['VAL'],
                  'FP'      : col_index_dict['FP'],
                  'EPN'     : col_index_dict['EPN'],
                }

            # Append item dict to bom list
            bom.append(d)




if __name__ == "__main__":


    csv_str = """Reference, Value, Footprint,EPN
    U1,XC9103,TO_SOT_Packages_SMD:SOT-23-5,XC9103_SOT23-5
    D1,MBR230LSFT1G,Diodes_SMD:SOD-123,MBR230LSFT1G_SOD123
    L1,10u,dong:5X5X4_BOURNS_INDUCTOR,IND_10U_2A_5X5
    R1,3K3,Resistors_SMD:R_0402,R_3K3_0402
    R3,10K,Resistors_SMD:R_0402,R_10K_0402
    R2,10K,Resistors_SMD:R_0402,R_10K_0402"""

    bom = BuildStandard(0)

    bom.process_csv(csv_str)

    pass