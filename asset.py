
# Library imports
import json
import time

class AssetDeletedError(Exception):
    pass
class AssetNotFoundError(Exception):
    pass


class AssetType(object):
    PART            = "*PART"
    BUILD_STANDARD  = "*BOM"


class Asset(object):

    def __init__(self, modules, fields=None, id=None):
        """
        Initialiser
        :param db:
        :param fields:
        :param id:
        :return:
        """

        # Init class vars
        self.modules    = modules
        self.db         = modules.database
        self._deleted   = False

        # If an ID has been passed, store it in the class
        if id:
            self.id = id

        # If fields have been passed, insert them
        elif fields:

            # Grab the time
            t = time.time()

            # Insert meta data into the fields dict
            fields['@meta'] = {'LAST_MODIFIED_TIME'     : t,
                               'LAST_MODIFYING_USER'    : 0,
                               'CREATION_TIME'          : t,
                               'EDITS_COUNT'            : 0,
                               }

            # Insert data into database, and grab the ID useed
            self.id = self.db.insert_one(fields).inserted_ids[0]

        # Without initial fields to create an entry, and no ID for an existing one, we can't create a local asset
        else:
            raise Exception("Asset init needs either fields or an ID.")

    def _get_field(self, field):
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

    def _get_fields(self, fields_list):
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

    def _get_dict(self, filter=None):
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

    def _get_json(self, filter=None):
        return json.dumps(self.get_dict(filter))

    def _set_field(self, field, value):

        if self._deleted:
            raise AssetDeletedError()

        self.db.update_one( { "_id"  : self.id },
                            { "$set" : { field : value, '@meta.LAST_MODIFIED_TIME' : time.time() },
                              "$inc" : { '@meta.EDITS_COUNT' : 1 }
                            }
                          )

    def delete(self):
        if self._deleted:
            raise AssetDeletedError()

        self.db.delete_one({'_id' : self.id})

