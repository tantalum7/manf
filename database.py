
# Library imports
from pymongo    import MongoClient
from time       import time

# Project imports
from asset import Asset, AssetNotFoundError

class Database(object):

    def __init__(self):

        #self.client = MongoClient("45.58.35.135", 80)
        self.client = MongoClient("45.58.35.135", 27027)

        print self.client.database_names()

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

        data = self.asset_collection.find_one(id)

        if not data:
            raise AssetNotFoundError()

        return Asset(db=self.asset_collection, id=str(id))

    def query(self, field_criteria, limit=1000):

        cursor = self.asset_collection.find(filter=field_criteria, projection=['_id'], limit=limit)

        return [Asset(db=self.asset_collection, id=result['_id']) for result in cursor]


if __name__ == "__main__":

    db = Database()

    #db.create_asset({"_id" : 9, "stuff" : "good"})

    print db.query({'_id' : 50} )

    a1 = db.get_asset(50)

    print a1.get_dict()

    print "Done"