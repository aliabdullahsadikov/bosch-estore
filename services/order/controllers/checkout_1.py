import datetime

import bson
from bson import ObjectId
from fastapi import HTTPException
from starlette import status

from common.database import get_db
from services.cart.controllers import UserCartManager
from services.order.controllers import OrderBaseController
from services.order.models.order import Order
from services.order.models.order_item import OrderItem
from services.order.modules.client.mongo_cart_client import MongoCartClient
from services.order.schemas.checkout import CheckoutSchema, CartItemInSchema, CartData, CartDataSchema
from services.cart.models.cart import Cart
from services.product.models.product import Product


class CheckoutOrderController(OrderBaseController):

    def __init__(self, payload: CheckoutSchema):
        self._payload = payload.dict()
        super(CheckoutOrderController, self).__init__(self._payload)

    def execute(self):

        cart_client = MongoCartClient()

        """ Check received cart_id """
        if not cart_client.valid_mongo_doc_id(self._payload['cart_id']):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Mongo document id is not valid {self._payload['cart_id']}"
            )

        """ checkout cart """
        if not cart_client.cart_check_and_set(self.user.id, self._payload['cart_id']):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cart not found by id {self._payload['cart_id']}"
            )

        """ Serialize cart document to CartDataSchema schema """
        cart: CartDataSchema = cart_client.serialize()

        """ Validation promo code """
        if self._payload["promo_code"]:
            if not self.valid_promo():
                self._payload["promo_code"] = None

        """ Checking order """
        if self.order_exist(cart):
            return self.response(
                status_code=status.HTTP_208_ALREADY_REPORTED,
                message="Order already created"
            )

        """ Create order according to cart data """
        order = self.create_order(cart)
        if not order:
            self.logger.exception("Order has not created")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Order has not created"
            )

        """ Create order items """
        order_items = self.create_order_items(order.id, cart.items)
        if not isinstance(order_items, bool) and isinstance(order_items, list):
            """ Execute cancelling, because it means has not created all items of order """
            CheckoutOrderController.cancel_items(order_items)
            CheckoutOrderController.cancel_order(order.id)
            return self.response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Order creation cancelled due to occurrence an error while saving items",
                error=True
            )

        """ Update cart status to ordered """
        cart_ordered = self.cart_ordered(cart.cart_id)
        if not cart_ordered:
            self.logger.exception("Error occurred while changing cart status")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while changing cart status"
            )

        return self.response(
            message="The order saved successfully",
            data={
                order
            }
        )

    def create_order_items(self, order_id: int, cart_items: list):
        """
        :param order_id:
        :param cart_items:
        :return:
        """
        created_items_ids = []
        for item in cart_items:
            item = item.dict()
            product = Product().get_active(item['product_id'])
            valid_amount = item["amount"] if product.check_amount(item["amount"]) else product.get_amount()
            sale = product.active_sale()
            sale_price_of_product = product.get_sale_price()

            with get_db() as db:
                order_item = OrderItem()
                order_item.order_id = order_id
                order_item.product_id = item['product_id']
                order_item.amount = valid_amount
                order_item.price = product.get_price()
                order_item.sale = sale.id if sale else None
                order_item.sale_percent = sale.percent if sale else 0
                order_item.sale_price = sale_price_of_product if sale_price_of_product else 0.0
                order_item.status = True
                order_item.created_at = datetime.datetime.now()

                db.add(order_item)
                db.commit()
                db.refresh(order_item)

                created_items_ids.append(order_item.id)

        return True if len(created_items_ids) == len(cart_items) else created_items_ids

    def cart_ordered(self, cart_id):
        query = {
            "_id": cart_id
        }
        set_data = {"$set": {"ordered": True}}
        result = Cart.update_one(query, set_data)

        return result if result else None

    @classmethod
    def cancel_order(cls, order_id) -> bool:
        with get_db() as db:
            order = db.get(Order, order_id)
            if order:
                db.delete(order)
                db.commit()
        return True

    @classmethod
    def cancel_items(cls, items_ids: list) -> None:
        with get_db() as db:
            for item_id in items_ids:
                order_item = db.get(OrderItem, item_id)
                if order_item:
                    db.delete(order_item)
                    db.commit()
