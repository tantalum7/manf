

import xlrd


def _XlsReaderHelper(xls_file, sheet_index=0, options=None):

    class _xls_reader(object):

        def __init__(self, xls_file_path, sheet_index=0, options=None):

            self.book       = xlrd.open_workbook(xls_file_path)
            self.sheet      = self.book.sheet_by_index(0)
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

    return _xls_reader(xls_file)

if __name__ == "__main__":


    xls = _XlsReaderHelper("M010-PCBA01-V1-12-BOM.xls")

    for x in range(3, 5000):
        line = xls.next()
        ref             = line[1]
        description     = line[2]
        manufacturer    = line[3]
        mpn             = line[4]
        print ref, description, manufacturer, mpn


    print "Done"