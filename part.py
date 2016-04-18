
# Library imports

# Project imports
from asset      import Asset, AssetType

 # Physical properties
        # -- Dimms
        # -- Footprint
        # -- Storage Temp
        # -- MSL etc
        # -- ROHS
        # Compliance data
        # -- ROHS
        # -- REACH etc
        # Electrical properties
        # -- Voltage/Current/Res/Cap etc etc
        # Alternative Parts data (merge into market data?)
        # Market Data (inc octopart scrape)
        # Docs
        # -- Datasheets, RoHS certificate, User guide etc

        # Core parameters
        # EPN
        # Status (End of Life, Suitable for new designs, unsuitable etc)
        # Description
        # Manufacturer
        # MPN


class PartAsset(object):

    PHYSICAL        = '@physical'
    COMPLIANCE      = '@compliance'
    ELECTRICAL      = '@electrical'
    ALTERNATIVES    = '@alternatives'
    MARKET          = '@market'
    DOCS            = '@docs'
    PART            = '@part'

    def __init__(self, db, id=None, fields=None):

        # If id and field is None, we are creating a new part from scratch. Prepare fields dict.
        if id is None and fields is None:
            fields = { '_type'          : AssetType.PART,
                       '@physical'      : {},
                       '@compliance'    : {},
                       '@electrical'    : {},
                       '@alternatives'  : {},
                       '@market'        : {},
                       '@docs'          : {},
                       '@part'          : { 'EPN'           : '',
                                            'STATUS'        : '',
                                            'DESCRIPTION'   : '',
                                            'MANUFACTURER'  : '',
                                            'MPN'           : '',
                                            'APPROVAL'      : '',
                                          },
                     }

        # Init class vars
        self._asset = Asset(db, fields=fields, id=id)

    def set_physical_parameter(self, parameter, value, unit=None):
        self._asset.set_field("@physical."+parameter, (value, unit))

    def set_electrical_parameter(self, parameter, value, unit=None):
        self._asset.set_field("@electrical."+parameter, (value, unit))

