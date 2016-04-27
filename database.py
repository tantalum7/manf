
# Library imports
from pymongo    import MongoClient
from bson       import objectid
from time       import time

# Project imports
from asset import Asset, AssetNotFoundError

class Database(object):

    def __init__(self, modules):

        # Store ref to modules
        self.modules = modules

        # Create db client object
        self.client = MongoClient("45.58.35.135", 27027)

        # Create ref to manf database collection
        self.db = self.client.manf_db

    @property
    def asset_collection(self):
        return self.db.assets

    def create_asset(self, fields={}):

        # Add standard fields
        fields['_creation_date'] = time()

        # Create the asset on the database, and return the local instance
        return Asset(db=self.asset_collection, fields=fields)

    def get_asset(self, id):

        id = objectid.ObjectId(str(id))

        data = self.asset_collection.find_one(id)

        if not data:
            raise AssetNotFoundError()

        return data

    def search_asset(self, field_criteria, limit=1000):

        cursor = self.asset_collection.find(filter=field_criteria, projection=['_id'], limit=limit)

        return [Asset(db=self.asset_collection, id=result['_id']) for result in cursor]

    def query(self, filter=None, projection=None):

        return   self.asset_collection.find(filter      = filter,
                                            projection  = projection,
                                            modifiers   = self.modules.settings.db_find_modifiers)

if __name__ == "__main__":

    from part import Part
    from constants  import Units
    db = Database()


    print "Done"