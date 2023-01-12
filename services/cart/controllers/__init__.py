import datetime
from uuid import UUID

import bson
from starlette import status

from common.database import get_db
from services import BaseController
from services.cart.models.cart import Cart
from services.product.models.product import Product
from services.user.auth import current_user

"""
To clarity, Cart module will work only with MongoDB (NoSQL) as a database.
However, we can use Sqlalchemy queries for an another models.
You can see Cart collection schema in the file "services/cart/models/cart.py"
"""


class CartBaseController(BaseController):

    def __init__(self):
        self.model = Cart
        super(CartBaseController, self).__init__()

    def _add(self):
        pass

    def _remove(self):
        pass

    def _clear(self):
        pass

    def _get_product_by_id(self) -> Product:
        """ sql query """
        with get_db() as db:
            product = db.query(Product).get(self.product_id)
            if product:
                product.photos = product.photos

        return product

    def _get_cart(self):
        """ no sql query """
        user_id = {
            "user_id": self.user.id
        }

        return self.model.find_one(user_id)

    def _get_product_by_id_nosql(self, product_id: int):
        """ no sql query """
        id = {
            "product_id": product_id
        }

        return self.model["products"].find_one(id)

    def _update_particular_product(self, query, set_data):
        return self.model.update_one(query, set_data)


class UserCartManager(object):

    STATUS = {
        "active": 0,
        "ordered": 1,
        "inactive": 2
    }

    def __init__(self):
        self.user = current_user()
        self.cart_collection = Cart
        self.active_cart = self._get_active_cart(self.user.id)
        self._has_active_cart = True if self.active_cart else False

    def create_cart(self, product: Product):
        """
        The method will create a new cart
        :param product: Product model
        :return:
        """
        new_cart = {
            "user_id": bson.Binary.from_uuid(self.user.id),
            "total": product.price,
            "ordered": False,
            "status": 0,
            "created_at": datetime.datetime.now(),
            "items": [
                    {
                        "product_id": product.id,
                        "product_name": product.name,
                        "article": product.model,
                        "price": product.price,
                        "amount": 1,
                        "total_price": product.price
                    }
                ]
            }
        inserted_id = self.cart_collection.insert_one(new_cart)

        return inserted_id

    def has_item(self, item_id: int):
        query = {
            "user_id": bson.Binary.from_uuid(self.user.id),
            "status": self.STATUS["active"],
            "items.product_id": item_id
        }
        result = self.cart_collection.find_one(query)

        return True if result else False

    def add(self, item_id):
        query = {
            "user_id": bson.Binary.from_uuid(self.user.id),
            "status": self.STATUS["active"],
            "items.product_id": item_id
        }
        cart = self.cart_collection.find_one(query)
        target_item = None
        for item in cart["items"]:
            if item.get("product_id") and item.get("product_id") == item_id:
                target_item = item

        result = None
        if target_item:
            target_item['amount'] = target_item["amount"] + 1
            target_item["total_price"] = target_item["amount"] * target_item["price"]
            set_data = {"$set": {"items.$": target_item}}

            result = self.cart_collection.update_one(query, set_data)

        return result if result else status.HTTP_500_INTERNAL_SERVER_ERROR

    def reduce(self, item_id):
        query = {
            "user_id": bson.Binary.from_uuid(self.user.id),
            "status": self.STATUS["active"],
            "items.product_id": item_id
        }
        cart = self.cart_collection.find_one(query)
        target_item = None
        for item in cart["items"]:
            if item.get("product_id") and item.get("product_id") == item_id:
                target_item = item

        result = None
        if target_item:
            if target_item['amount'] > 0:
                target_item['amount'] = target_item["amount"] - 1
                target_item["total_price"] = target_item["amount"] * target_item["price"]

                set_data = {"$set": {"items.$": target_item}}
                result = self.cart_collection.update_one(query, set_data)
            else:
                self.remove_item(item_id)
                return True

        """ checkout item amount after reduction, if item amount become 0 bellow line will remove this item """
        if target_item["amount"] <= 0:
            self.remove_item(item_id)

        return result if result else status.HTTP_500_INTERNAL_SERVER_ERROR

    def remove_cart(self):
        query = {
            "user_id": bson.Binary.from_uuid(self.user.id),
            "status": self.STATUS["active"],
        }
        set_data = {"$set": {"status": self.STATUS["inactive"]}}
        result = self.cart_collection.update_one(query, set_data)

        return result if result else status.HTTP_500_INTERNAL_SERVER_ERROR

    def remove_item(self, item_id):
        query = {
            "user_id": bson.Binary.from_uuid(self.user.id),
            "status": self.STATUS["active"],
            "items.product_id": item_id
        }
        set_data = { "$pull": {"items": {"product_id": item_id}}}
        result = self.cart_collection.update_one(query, set_data)

        return result if result else status.HTTP_500_INTERNAL_SERVER_ERROR

    def create_item(self, product: Product):
        query = {
            "user_id": bson.Binary.from_uuid(self.user.id),
            "status": self.STATUS["active"]
        }
        cart = self.cart_collection.find_one(query)
        if cart['items']:
            items = cart['items']
            items.append({
                        "product_id": product.id,
                        "product_name": product.name,
                        "article": product.model,
                        "price": product.price,
                        "amount": 1,
                        "total_price": product.price
                    })
        else:
            cart['items'] = [{
                "product_id": product.id,
                "product_name": product.name,
                "article": product.model,
                "price": product.price,
                "amount": 1,
                "total_price": product.price
            }]

        set_data = {
            "$set": {
                "items": cart['items']
            }
        }
        result = self.cart_collection.update_one(query, set_data)

        return result

    def _get_active_cart(self, user_id):
        """ no sql query """
        bson.Binary.from_uuid(self.user.id)
        query = {
            "user_id": bson.Binary.from_uuid(self.user.id),
            "ordered": False,
            "status": self.STATUS["active"]
        }
        return self.cart_collection.find_one(query)

    def inactivate_cart(self) -> None:
        query = {"user_id": self.user.id}
        set_data = {"$set": {"status": self.STATUS['inactive']}}
        updated = self.cart_collection.update_one(query, set_data)

    # def __repr__(self):
    #     return self.__repr__()
