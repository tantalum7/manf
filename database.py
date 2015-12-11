
# Library imports
from pymongo    import MongoClient
from datetime   import datetime

# Project imports
from asset import Asset

class Database(object):

    def __init__(self):

        self.client = MongoClient("45.58.35.135", 27027)

        self.client.database_names()

        self.db = self.client.manf_db

    @property
    def asset_collection(self):
        return self.db.assets

    def create_asset(self, fields):

        # Add standard fields
        fields['_creation_date'] = datetime.utcnow()

        # Create the asset on the database, and return the local instance
        return Asset(db=self.asset_collection, fields=fields)

    def query(self, field_criteria, limit=1000):

        cursor = self.asset_collection.find(filter=field_criteria, projection=['_id'], limit=limit)

        return [Asset(db=self.asset_collection, id=result['_id']) for result in cursor]
