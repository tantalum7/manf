
# Library imports
import csv
import xlrd
from collections    import Iterator

# Project imports
from asset      import Asset, AssetType
from util_funcs import recursive_dict_update


def _CsvReaderFactory(csv_data_string=None, csv_file_path=None):

    class _dialect(csv.Dialect):
        def __init__(self):

            self.skipinitialspace   = True
            self.delimiter          = ','
            self.quotechar          = '|'
            self.quoting            = csv.QUOTE_MINIMAL
            self.lineterminator     = "\r\n"
            csv.Dialect.__init__(self)


    if csv_data_string is None and csv_file_path is not None:
        csv_data_string = open(csv_file_path).read()

    elif csv_file_path is None and csv_data_string is None:
        raise Exception("No csv data string or file path provided")


    return csv.reader(csv_data_string.splitlines(), dialect=_dialect())


def _XlsReaderFactory(xls_file_path=None, xls_file_contents=None, sheet_index=0, options=None):

    class _xls_reader(Iterator):

        def __init__(self, xls_file_path=None, xls_file_contents=None, sheet_index=0, options=None):

            self.book       = xlrd.open_workbook(filename=xls_file_path, file_contents=xls_file_contents)
            self.sheet      = self.book.sheet_by_index(sheet_index)
            self.row_index  = 0

        def next(self):

            # Try and grab list of cell objects at row index position
            try:
                cell_obj_list = self.sheet.row(self.row_index)

            # Catch index error exception, and reraise as stop iteration exception
            except IndexError:
                raise StopIteration

            # Push any other exceptions further up
            except:
                raise

            # Continue parsing row data
            else:

                # Increment row index
                self.row_index += 1

                # Grab the value of the cell objects only, and return as list
                return [cell.value for cell in cell_obj_list]

    if xls_file_path is None and xls_file_contents is None:
        raise Exception("No csv data string or file path provided")

    return _xls_reader(xls_file_path=xls_file_path, xls_file_contents=xls_file_contents, sheet_index=sheet_index)


class BuildStandard(Asset):

    CSV_FILE            = "CSV"
    XLS_FILE            = "XLS"

    _CSV_COL_REF        = ["REF", "Reference", "REFERENCE", "Ref"]
    _CSV_COL_VALUE      = ["VAL", "Value", "VALUE", "Val"]
    _CSV_COL_FOOTPRINT  = ["FP", "Footprint", "FOOTPRINT"]
    _CSV_COL_EPN        = ["EPN", "epn", "Engineering Part Number"]
    _CSV_COL_DNF        = ["DNF", "dnf", "DO NOT FIT", "Do not fit"]

    _FIELD_BOM          = "@bom"
    _FIELD_DATA         = "@data"
    _FELD_HISTORY       = "@history"

    def __init__(self, app, id=None, fields=None):

        # Define default fields dict
        default = { '_type'          : AssetType.BUILD_STANDARD,
                    '@history'       : {},
                    '@data'          : {},
                    '@bom'           : { 'NAME'         : '',
                                         'STATUS'       : '',
                                         'DESCRIPTION'  : '',
                                         'REVISION'     : '',
                                         'APPROVAL'     : '',
                                         'BOM_TYPE'     : '',
                                      },
                 }

        # If a fields dict was passed, update the default dict with it
        if fields:
            default = recursive_dict_update(default, fields)

        # Init parent class
        #Asset.__init__(self, app=app, fields=default, id=id)

    @property
    def name(self):
        return self._get_field(self._FIELD_BOM).get("NAME")

    @name.setter
    def name(self, a):
        self._set_field('.'.join([self._FIELD_BOM, 'NAME']), str(a))

    @property
    def description(self):
        return self._get_field(self._FIELD_BOM).get("DESCRIPTION")

    @description.setter
    def description(self, a):
        self._set_field('.'.join([self._FIELD_BOM, 'DESCRIPTION']), str(a))

    @property
    def revision(self):
        return self._get_field(self._FIELD_BOM).get("REVISION")

    @revision.setter
    def revision(self, a):
        self._set_field('.'.join([self._FIELD_BOM, 'REVISION']), str(a))

    @property
    def data(self):
        return self._get_field(self._FIELD_DATA).get("variant_zero")

    def process_engineering_bom(self, file_type, file_path=None, file_contents_string=None):

    def _process_bom(self, file_type, file_path=None, file_contents_string=None, headings_list=None):

        # Check if file type is csv
        if file_type is self.CSV_FILE:

            # Create csv reader object
            reader = _CsvReaderFactory(csv_file_path=file_path, csv_data_string=file_contents_string)

        # Check if file type is xls
        elif file_type is self.XLS_FILE:

            # Create xls reader object
            reader = _XlsReaderFactory(xls_file_path=file_path, xls_file_contents=file_contents_string)

        # No valid file type passed, raise exception
        else:
            raise Exception("No valid file type passed ({})".format(str(file_type)))

        # Parse the csv into a dict
        bom_list = self._parse_bom(reader)

        return bom_list

        # Lookup the bom items in the database, and match to known parts (in place operation)
        #self._bom_database_lookup(bom_list)

        # Store the Bom in the DB under data, then variant_zero (variant system TBD)
        #self._set_field(".".join([self._FIELD_DATA, "variant_zero"]), bom_list)

    def _parse_bom(self, reader):

        # Prepare list of column headings we are looking for (list of list of spelling variants)
        col_headings_list = [self._CSV_COL_REF, self._CSV_COL_VALUE, self._CSV_COL_EPN,
                             self._CSV_COL_FOOTPRINT, self._CSV_COL_DNF]

        # Prepare dict to store the index location of the headings, and headings found flag
        col_index_dict = {}
        headings_found = False

        # Iterate through the first 5 lines to try and find the headings properly
        for x in range(5):

            # Grab the first line which should be the column headings
            columns = reader.next()

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

            # If we managed to find all the column headings, set the found headings flag and break from the loop
            if len(col_index_dict.keys()) > 3:
                headings_found = True
                continue

        # If we get this far, and haven't found the column headings we should raise an exception
        if not headings_found:
            raise Exception("Cannot find required column headings ({})".format(str(col_index_dict)))

        # Prepare empty bom list
        bom = []

        # Iterate through the rest of the csv
        for line in reader:

            # Create a temp bom item object to store bom item's data
            d = { 'REF'     : line[ col_index_dict['REF'] ],
                  'VALUE'   : line[ col_index_dict['VAL'] ],
                  #'FP'      : line[ col_index_dict['FP']  ],
                  'EPN'     : line[ col_index_dict['EPN'] ],
                }

            # Append item dict to bom list
            bom.append(d)

        # Return the bom list
        return bom

    def _bom_database_lookup(self, bom_list):

        # Create an empty dict of unique parts
        # (so we don't do expensive database lookups for repeated bom parts)
        unique_parts = {}

        # Iterate through bom items
        for item in bom_list:

            # Check if the item isn't already in the unique parts dict
            if item['EPN'] not in unique_parts:

                # Try and fetch the item EPN in the database, and store it's ID in the unqiue parts dict
                try:
                    part = self.app.factory.fetch_part(item['EPN'])
                    unique_parts[ item['EPN'] ] = str(part.id)

                # If we can't find the part in the database, set the ID for this EPN as None
                except self.app.NotFoundError:
                    unique_parts[ item['EPN'] ] = None

                # Push any other exception up further
                except:
                    raise

            # Store the db part id in the item dict
            item['DB_ID'] = unique_parts[ item['EPN'] ]

        pass

if __name__ == "__main__":


    csv_str = """Reference, Value, Footprint,EPN
    U1,XC9103,TO_SOT_Packages_SMD:SOT-23-5,XC9103_SOT23-5
    D1,MBR230LSFT1G,Diodes_SMD:SOD-123,MBR230LSFT1G_SOD123
    L1,10u,dong:5X5X4_BOURNS_INDUCTOR,IND_10U_2A_5X5
    R1,3K3,Resistors_SMD:R_0402,R_3K3_0402
    R3,10K,Resistors_SMD:R_0402,R_10K_0402
    R2,10K,Resistors_SMD:R_0402,R_10K_0402"""

    bom = BuildStandard(0)

    b1 = bom.process_engineering_bom(file_type=bom.CSV_FILE, file_contents_string=csv_str)

    b2 = bom.process_bom(file_type=bom.XLS_FILE, file_path="experiments\M010-PCBA01-V1-12-BOM.xls")

    pass