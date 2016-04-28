
# Library imports
import  collections

# Project imports
from asset      import Asset, AssetType
from util_funcs import recursive_dict_update

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


class Part(Asset):

    PHYSICAL        = '@physical'
    COMPLIANCE      = '@compliance'
    ELECTRICAL      = '@electrical'
    ALTERNATIVES    = '@alternatives'
    MARKET          = '@market'
    DOCS            = '@docs'
    PART            = '@part'

    def __init__(self, db, id=None, fields=None):

        default = { '_type'          : AssetType.PART,
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
                                         'COMPONENT_TYPE': '',
                                      },
                 }

        # If a fields dict was passed, update the default dict with it
        if fields:
            default = recursive_dict_update(default, fields)

        # Init parent class
        Asset.__init__(self, db, fields=default, id=id)

    @property
    def EPN(self):
        return self._get_field(self.PART).get('EPN')

    @EPN.setter
    def EPN(self, a):
        self._set_field('.'.join([self.PART, 'EPN']), str(a))

    @property
    def description(self):
        return self._get_field(self.PART).get('DESCRIPTION')

    @description.setter
    def description(self, a):
        self._set_field('.'.join([self.PART, 'DESCRIPTION']), str(a))

    @property
    def component_type(self):
        return self._get_field(self.PART).get('COMPONENT_TYPE')

    @component_type.setter
    def component_type(self, a):
        self._set_field('.'.join([self.PART, 'COMPONENT_TYPE']), str(a))

    @property
    def manufacturer(self):
        return self._get_field(self.PART).get('MANUFACTURER')

    @manufacturer.setter
    def manufacturer(self, a):
        self._set_field('.'.join([self.PART, 'MANUFACTURER']), str(a))

    @property
    def MPN(self):
        return self._get_field(self.PART).get('MPN')

    @MPN.setter
    def MPN(self, a):
        self._set_field('.'.join([self.PART, 'MPN']), str(a))

    @property
    def approval(self):
        return self._get_field(self.PART).get('APPROVAL')

    @property
    def status(self):
        return self._get_field(self.PART).get('STATUS')

    def set_physical_parameter(self, parameter, value, unit=None):
        self._set_field('.'.join([self.PHYSICAL, parameter]), (value, str(unit)))

    def set_electrical_parameter(self, parameter, value, unit=None):
        self._set_field("@electrical."+parameter, (value, unit))




