

class Constants(object):

    def __init__(self, app):

        # Store ref to top level app
        self.app = app

        # Load units from db
        self.load_units_from_db()

    def load_units_from_db(self):

        # Fetch data entry from db
        db_data = self.app.database.find_one({"_type" : "*UNITS"})

        # Grab units and store in class
        self.electrical_units   = db_data.get("@electrical")
        self.physical_units     = db_data.get("@physical")
        self.si_prefixes        = db_data.get("@si_prefixes")
        self.bin_prefixes       = db_data.get("@bin_prefixes")
        self.prefixes           = {}
        self.prefixes.update(self.si_prefixes)
        self.prefixes.update(self.bin_prefixes )

    def get_dict(self):
        return { 'electrical_units' : self.electrical_units,
                 'physical_units'   : self.physical_units,
                 'si_prefixes'      : self.si_prefixes,
                 'bin_prefixes'     : self.bin_prefixes,
                 'prefixes'         : self.prefixes,
               }