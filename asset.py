
# Library imports
import json

class AssetDeletedError(Exception):
    pass
class AssetNotFoundError(Exception):
    pass

class Asset(object):

    def __init__(self, db, fields=None, id=None):
        """
        Initialiser
        :param db:
        :param fields:
        :param id:
        :return:
        """
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
        Returns the value of an asset field

        :param field:
        :return:
        """
        # If the asset has been deleted, throw an exception
        if self._deleted:
            raise AssetDeletedError()

        # Grab asset data from db
        data = self.db.find_one(self.id)

        # If no valid data found, throw an exception
        if not data:
            return AssetNotFoundError()

        # Return the field from the data dict
        return data.get(field)

    def get_fields(self, fields_list):
        """
        Returns a dict with field : value for every field in the list argument. Any fields requested
        in the list that do not exist in the asset will have value None in the dictionary.

        :param fields_list:
        :return fields_dict
        """
        # If the asset has been deleted, throw an exception
        if self._deleted:
            raise AssetDeletedError()

        # Grab asset data from db
        asset_data = self.db.find_one(self.id)

        # If the asset cannot be found, throw an exception
        if not asset_data:
            raise

        # Create a dict with keys from fields_list (value None)
        fields_dict = {}.fromkeys(fields_list)

        # Return a subset dict of asset_data with keys from the fields list
        return dict((field, asset_data.get(field)) for field in fields_list)

    def get_dict(self, filter=None):
        """

        :param filter:
        :return:
        """
        # If the asset has been deleted, throw an exception
        if self._deleted:
            raise AssetDeletedError()

        # Grab asset data from db, if a filter arg was passed apply to search
        if filter:
            asset_data = self.db.find_one(self.id, projection=filter)
        else:
            asset_data = self.db.find_one(self.id)

        # If the asset cannot be found, throw an exception
        if not asset_data:
            raise

        # Return dict
        return asset_data

    def get_json(self, filter=None):
        return json.dumps(self.get_dict(filter))

    def set_field(self, field, value):

        if self._deleted:
            raise AssetDeletedError()

        #if field in self.get_fields_list():
        self.db.update_one({"_id" : self.id}, {"$set":{field : value}})

    def get_fields_list(self):
        if self._deleted:
            raise AssetDeletedError()

        return self.db.find_one(self.id).keys()

    def delete(self):
        if self._deleted:
            raise AssetDeletedError()

        self.db.delete_one({'_id' : self.id})

