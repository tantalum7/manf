

class AssetDeletedError(Exception):
    pass


class Asset(object):

    def __init__(self, db, fields=None, id=None):

        # Init class vars
        self.db         = db
        self._deleted   = False

        # If fields have been passed, insert them
        if fields:
            self.id = self.db.insert_one(fields).inserted_id

        # If an ID has been passed, store it in the class
        elif id:
            self.id = id

        # Without initial fields to create an entry, and no ID for an existing one, we can't create a local asset
        else:
            raise Exception("Asset init needs either fields or an ID.")

    def get_field(self, field):
        """
        Returns the value of a field
        :param field:
        :return:
        """
        if self._deleted:
            raise AssetDeletedError()
        return self.db.find_one(self.id)[field]

    def set_field(self, field, value):

        if self._deleted:
            raise AssetDeletedError()

        if field in self.get_fields():
            self.db.update_one({"_id" : self.id}, {"$set":{field : value}})

    def get_fields_list(self):
        if self._deleted:
            raise AssetDeletedError()

        return self.db.find_one(self.id).keys()

    def delete(self):
        if self._deleted:
            raise AssetDeletedError()

        self.db.delete_one({'_id' : self.id})
