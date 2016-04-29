
# Library imports

# Project imports
from part       import Part
from asset      import Asset, AssetType
from bom        import BuildStandard


class Factory(object):

    def __init__(self, modules):

        # Store modules ref
        self.modules = modules

    def create_part(self, id=None, fields=None):
        return Part(self.modules, id, fields)

    def create_asset(self, id=None, fields=None):
        return Asset(self.modules, id, fields)

    def create_build_standard(self, id=None, fields=None):
        return BuildStandard(self.modules, id, fields)

    def _parse_database_dict(self, database_dict):

        if database_dict.get("_type") == AssetType.PART:
            return self.create_part(id=database_dict['_id'])