import bson
from bson import ObjectId

from services.cart.controllers import UserCartManager
from services.cart.models.cart import Cart
from services.order.schemas.checkout import CartDataSchema


class MongoCartClient(object):

    def __init__(self):
        self._document = Cart
        self._status = UserCartManager.STATUS
        self._current = None

    @staticmethod
    def valid_mongo_doc_id(cart_id) -> bool:
        return ObjectId.is_valid(cart_id)

    def cart_check_and_set(self, user_id, cart_id: ObjectId) -> bool:
        """ checking cart """
        query = {
            "user_id": bson.Binary.from_uuid(user_id),
            "_id": ObjectId(cart_id),
            "status": self._status["active"],
            "ordered": False,
        }
        result = self._document.find_one(query)

        if result:
            self._current = result
            return True

        return False

    def serialize(self) -> CartDataSchema:
        data = CartDataSchema(
            cart_id=str(self._current["_id"]),
            cart_data=self._current,
            items=self._current["items"]
        )

        return data
