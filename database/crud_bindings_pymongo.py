
# Library imports
from pymongo    import MongoClient, ASCENDING, DESCENDING
from bson       import objectid
from time       import time

# Project imports
from asset import Asset, AssetNotFoundError

class OperationResult(object):

    def __init__(self, success=False, op_count=None, message=None, inserted_ids=None, modified_ids=None):

        # Init class vars
        self.success        = success
        self.op_count       = op_count
        self.message        = message
        self.inserted_ids   = inserted_ids
        self.modified_ids   = modified_ids

    @property
    def success(self):
        return self._success

    @success.setter
    def success(self, value):
        self._success = bool(value)

    @property
    def op_count(self):
        return self._op_count

    @op_count.setter
    def op_count(self, value):
        self._op_count = None if value is None else int(value)

    @property
    def inserted_ids(self):
        return self._inserted_ids

    @inserted_ids.setter
    def inserted_ids(self, value):
        self._inserted_ids = [] if value is None else list(value)

    @property
    def modified_ids(self):
        return self._modified_ids

    @modified_ids.setter
    def modified_ids(self, value):
        self._modified_ids = [] if value is None else [value]

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = None if value is None else str(value)

    def __nonzero__(self):
        return bool(self.success)


class SearchResult(object):

    def __init__(self, pymongo_cursor):
        self._pymongo_cursor = pymongo_cursor

    def __getitem__(self, *args):
        return self._pymongo_cursor.__getitem__(*args)

    def __len__(self):
        return self._pymongo_cursor.count()
    #
    # def __iter__(self):
    #     return self._pymongo_cursor.next()

    def __nonzero__(self):
        return bool( self.__len__() )

    def sort(self, field, ascending=True):
        self._pymongo_cursor.sort(field, ASCENDING if ascending else DESCENDING)

    def as_list(self):
        return [data for data in self]


class Database(object):

    def __init__(self, ip_port_tuple):

        # Create db client object
        self.client = MongoClient(*ip_port_tuple)

        # Create ref to manf database assets collection
        self.db = self.client.manf_db.assets

    # CRUD

    def update_one(self, filter, data):
        mongo_result = self.db.update_one(filter=filter, update=data, upsert=False)
        return OperationResult(success  = mongo_result.acknowledged,
                               op_count = mongo_result.modified_count)

    def update_many(self, filter, data):
        mongo_result = self.db.update_many(filter=filter, update=data, upsert=False)
        return OperationResult(success  = mongo_result.acknowledged,
                               op_count = mongo_result.modified_count)

    def find_one(self, filter=None, projection=None, sort=None):
        return self.db.find_one(filter=filter, projection=projection, sort=sort)

    def find_many(self, filter=None, projection=None, limit=0, sort=None):
        return SearchResult( self.db.find(filter=filter, projection=projection, limit=limit, sort=sort) )

    def insert_one(self, data):
        mongo_result = self.db.insert_one(document=data)
        return OperationResult(success      = mongo_result.acknowledged,
                               op_count     = 1 if mongo_result.acknowledged else 0,
                               inserted_ids = [mongo_result.inserted_id])

    def insert_many(self, data_set):
        mongo_result = self.db.insert_many(documents=data_set)
        return OperationResult(success      = mongo_result.acknowledged,
                               op_count     = len(mongo_result.inserted_ids),
                               inserted_ids = mongo_result.inserted_ids)

    def delete_one(self, filter):
        mongo_result = self.db.delete_one(filter=filter)
        return OperationResult(success  = mongo_result.acknowledged,
                               op_count = mongo_result.deleted_count)

    def delete_many(self, filter):
        mongo_result = self.db.delete_many(filter=filter)
        return OperationResult(success  = mongo_result.acknowledged,
                               op_count = mongo_result.deleted_count)

    def id(self, id_string):
        return id_string if isinstance(id_string, objectid.ObjectId) else objectid.ObjectId(id_string)

if __name__ == "__main__":

    from part import Part
    from constants import Units
    db = Database(0)




    print "Done"