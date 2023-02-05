import bson
from bson import ObjectId
from pymongo import MongoClient


class MongoCoreClient:

    def __init__(
            self,
            mongo_client: MongoClient,
            mongo_db,
            document=None,
    ):
        self._mongo_client = mongo_client
        self._mongo_db = mongo_db
        self._document = document

    @property
    def document(self):
        return self._document

    @document.setter
    def document(self, value):
        self._document = value

    @staticmethod
    def valid_id(_id) -> bool:
        """ Will check out that the id is an ObjectId instance or not """
        return ObjectId.is_valid(_id)

    def document_exist(self, **kwargs) -> bool:
        """ Document checking """
        result = self._document.find_one(kwargs)

        return True if result else False

    def get_document(self, **kwargs):
        """ Get document """
        return self._document.find_one(kwargs)

    def update(self, query, value):
        """ Update document """
        return self._document.update_one(query, value)
