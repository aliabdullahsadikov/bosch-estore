import datetime

import bson
from bson import ObjectId
from fastapi import HTTPException
from starlette import status

from common.get_db import get_db
from services.cart.controllers import UserCartManager
from services.order.controllers import OrderBaseController
from services.order.models.order import Order, ORDER_STATUS
from services.order.models.order_item import OrderItem
from services.order.modules.order.order_manager import OrderManager
from services.order.schemas.checkout import CheckoutSchema, CartItemInSchema, CartDataSchema
from services.cart.models.cart import Cart
from services.order.schemas.order_in import OrderItemInSchema
from services.order.schemas.order_out import OrderOutSchema
from services.product.models.product import Product
from services.product.modules.product_manager import ProductManager


class CheckoutOrderController(OrderBaseController):

    def __init__(self, payload: CheckoutSchema):
        self._payload = payload.dict()
        super(CheckoutOrderController, self).__init__(self._payload)
        self._mongo_client.document = Cart

    def execute(self):

        """ Check received cart_id """
        if not self.valid_mongo_doc_id():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Mongo document id is not valid {self._payload['cart_id']}"
            )

        """ checkout cart """
        if not self.cart_exist():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cart not found by id {self._payload['cart_id']}"
            )

        """ get cart from mongodb """
        cart = self.get_cart()

        """ Validation promo code """
        if self._payload["promo_code"]:
            if not self.valid_promo():
                self._payload["promo_code"] = None

        order_manager = OrderManager()

        """ Checking order """
        if order_manager.check_by_cart_id(cart.cart_id):
            if (
                    order_manager.get_order_status() != ORDER_STATUS.get("unprocessed")
                    and order_manager.get_order_status() != ORDER_STATUS.get("canceled")
            ):
                return self.response(
                    status_code=status.HTTP_208_ALREADY_REPORTED,
                    message="Order already created"
                )

        """ Create order according to cart data """
        order_manager.create(cart, self.user.id, self.payload)
        if not order_manager.object:
            self.logger.exception("Order has not created")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Order has not created"
            )

        """ Create order items """
        for item in cart.items:
            order_item = self.prepare_item_to_save(order_manager, item)
            order_manager.add_item(order_item)

        if order_manager.count_items() != len(cart.items):
            """ Execute cancelling, because it means has not created all items of order """
            order_manager.make_unprocessed()
            return self.response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Order creation cancelled due to occurrence an error while saving items",
                error=True
            )

        order_manager.save_items()

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
            data=OrderOutSchema.from_orm(order_manager.refresh_object()).dict()
        )

    def prepare_item_to_save(self, order_manager, item):
        """ get product """
        product = self.get_product_by_id(item.product_id)
        sale = None
        sale_price = None
        if product:
            """ Serialize items """
            order_item = OrderItemInSchema(
                order_id=order_manager.object.id,
                product_id=item.product_id,
                amount=item.amount,
                price=product.price,
                sale_percent=sale,
                sale_price=sale_price,
                # total_price=order_manager.calculate_item_total_price(item.amount, product.price)
            )
        else:
            order_item = OrderItemInSchema(
                order_id=order_manager.object.id,
                product_id=item.product_id,
                amount=item.amount,
            )
        return order_item

    def get_product_by_id(self, product_id) -> Product:
        with get_db() as db:
            product = db.query(Product).get(product_id)
            product.photos = product.photos

        return product

    def get_order(self, order_id):
        with get_db() as db:
            order = db.query(Order).get(order_id)
            order.items = order.items

        return order

    def cart_exist(self):
        query = {
            "user_id": bson.Binary.from_uuid(self.user.id),
            "_id": ObjectId(self._payload['cart_id']),
            "status": UserCartManager.STATUS["active"],
            "ordered": False,
        }
        return self._mongo_client.document_exist(**query)

    def get_cart(self) -> CartDataSchema:
        """
        Used MongoDB query to receive cart
        :return:
        """
        query = {
            "user_id": bson.Binary.from_uuid(self.user.id),
            "_id": ObjectId(self._payload['cart_id']),
            "status": UserCartManager.STATUS["active"],
            "ordered": False,
        }
        cart = self._mongo_client.get_document(**query)

        schema = CartDataSchema(
            cart_id=str(cart["_id"]),
            cart_data=cart,
            items=cart["items"]
        )

        return schema

    def cart_ordered(self, cart_id):
        query = {
            "_id": cart_id
        }
        set_data = {"$set": {"ordered": True}}
        result = self._mongo_client.update(query, set_data)

        return result if result else None

    def cart_cancelled(self, cart_id):
        query = {
            "_id": cart_id
        }
        set_data = {"$set": {"ordered": False, "status": -1}}
        result = self._mongo_client.update(query, set_data)

        return result if result else None

    def valid_mongo_doc_id(self) -> bool:
        return self._mongo_client.valid_id(self._payload["cart_id"])

    # @classmethod
    # def cancel_order(cls, order_id) -> bool:
    #     with get_db() as db:
    #         order = db.get(Order, order_id)
    #         if order:
    #             db.delete(order)
    #             db.commit()
    #     return True

    @classmethod
    def cancel_items(cls, items_ids: list) -> None:
        with get_db() as db:
            for item_id in items_ids:
                order_item = db.get(OrderItem, item_id)
                if order_item:
                    db.delete(order_item)
                    db.commit()

#   def create_order_items(self, order: Order, cart_items: list):
#     """
#     :param order_id:
#     :param cart_items:
#     :return:
#     """
#     created_items_ids = []
#     sub_total: float = 0.0
#     total_price: float = 0.0
#     for item in cart_items:
#         item = item.dict()
#         product = ProductManager()
#         product = Product().get_active(item['product_id'])
#         valid_amount = item["amount"] if product.check_amount(item["amount"]) else product.get_amount()
#         sale = self.active_sale()
#         sale_price_of_product = self.get_sale_price()
#
#         with get_db() as db:
#             order_item = OrderItem()
#             order_item.order_id = order.id
#             order_item.product_id = item['product_id']
#             order_item.amount = valid_amount
#             order_item.price = product.get_price()
#             order_item.sale = sale.id if sale else None
#             order_item.sale_percent = sale.percent if sale else 0
#             order_item.sale_price = sale_price_of_product if sale_price_of_product else 0.0
#             order_item.status = True
#             order_item.created_at = datetime.datetime.now()
#
#             db.add(order_item)
#             db.commit()
#             db.refresh(order_item)
#
#             sub_total = sub_total + order_item.price * order_item
#             total_price = total_price +
#             # order_update = db.query(Order)\
#             #     .filter(Order.id == order.id)\
#             #     .update(sub_total=)
#
#             created_items_ids.append(order_item.id)
#
#     return True if len(created_items_ids) == len(cart_items) else created_items_ids