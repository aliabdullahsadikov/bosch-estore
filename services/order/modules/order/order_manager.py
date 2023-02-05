import logging
from abc import ABC, abstractmethod

from common.database import get_db
from logs.log_base import file_error_handler
from services.order.models.order import Order, ORDER_STATUS
from services.order.models.order_item import OrderItem
from services.order.schemas.checkout import CartDataSchema, CartItemInSchema
from services.order.schemas.order_in import OrderItemInSchema
from services.product.models.product import Product


class OrderManager(object):

    def __init__(self):
        self._model = Order
        self._order_obj = None
        self._items: list = []

    @property
    def object(self):
        return self._order_obj

    @object.setter
    def object(self, order_id):
        self._order_obj = self._get_order(order_id)

    def _get_order(self, order_id: int):
        with get_db() as db:
            order = db.query(Order).filter(Order.id == order_id).first()
            if order:
                order.items = order.items
                return order

        return None

    def refresh_object(self):
        with get_db() as db:
            order = db.query(Order).filter(Order.id == self._order_obj.id).first()
            if order:
                order.items = order.items
                return order

    def check_by_cart_id(self, cart_id: str) -> bool:
        """ This method can be used in checkout operation in order to create on order once """
        with get_db() as db:
            order = db.query(Order).filter(Order.cart_id == cart_id).first()
            if order:
                order.items = order.items
                self._order_obj = order
                return True

        return False

    def get_order_status(self):
        return self.object.status

    def create(self, cart: CartDataSchema, user_id: int, payload: dict):
        """
        Method will receive cart as a mongo object
        :param cart:
        :return:
        """
        with get_db() as db:
            order = self._model()
            order.cart_id = str(cart.cart_id)
            order.user_id = user_id
            order.promo_code = payload['promo_code']

            db.add(order)
            db.commit()
            db.refresh(order)

        self._order_obj = order if order else None

        return order

    def save_items(self):
        if len(self._items) > 0:
            try:
                for item in self._items:
                    self._save_item(item.dict())
            except Exception as exc:
                logger = self._get_logger()
                logger.exception("Order items not created successfully")
            finally:
                return True

    def _save_item(self, item):
        with get_db() as db:
            order_item = OrderItem(**item)
            db.add(order_item)
            db.commit()

    def add_item(self, item: OrderItemInSchema) -> None:
        self._items.append(item)

    def count_items(self):
        return len(self._items)

    def calculate_item_total_price(self, amount, price):
        return amount * price

    def _get_logger(self):
        logger = logging.getLogger(self.__module__)
        logger.addHandler(file_error_handler)
        return logger

    def make_unprocessed(self):
        with get_db() as db:
            order = db.query(self._model)\
                .filter(self._model.id == self._order_obj.id)\
                .first()
            order.status = ORDER_STATUS["unprocessed"]
            db.commit()

    #  shujoyini qilish kere

