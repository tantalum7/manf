
# Library imports

# Project imports
from part       import Part
from asset      import Asset, AssetType
from bom        import BuildStandard


class Factory(object):

    def __init__(self, app):

        # Store ref to top level app
        self._app = app

    def create_part(self, id=None, fields=None):
        return Part(self._app, id, fields)

    def create_asset(self, id=None, fields=None):
        return Asset(self._app, id, fields)

    def create_build_standard(self, id=None, fields=None):
        return BuildStandard(self._app, id, fields)

    def fetch_part(self, epn):

        # Search database for EPN
        part_dict = self._app.database.find_one(filter={'@part.EPN' : epn})

        # If we received a valid result dict, create and return a Part object for this EPN
        if part_dict:
            return self.create_part(id=part_dict['_id'])

        # Could not find a part with the EPN, raise an exception
        else:
            raise self._app.NotFoundError()

    def _parse_database_dict(self, database_dict):

        if database_dict.get("_type") == AssetType.PART:
            return self.create_part(id=database_dict['_id'])