from abc import abstractmethod

from common.database import get_db
from services import current_user
from services.order.models.order import Order
from services.order.modules.order.order_manager import OrderManager
from services.order.schemas.checkout import CartDataSchema


class OrderSubManager(OrderManager):

    def __init__(self, cart: CartDataSchema):
        self._cart = cart
        self._instance = None
        self._model = Order
        self._items = []
        self.user = current_user()
        super(OrderSubManager, self).__init__()

    def is_exist(self) -> bool:
        with get_db() as db:
            order = db.query(Order)\
                .filter(Order.cart_id == self._cart.cart_id)\
                .first()

        return True if order else False

    def create(self):
        """
         Method will receive cart as a mongo object
         :param cart:
         :return:
         """
        with get_db() as db:
            order = self._model()
            order.cart_id = str(self._cart.cart_id)
            order.user_id = self.user.id
            order.promo_code = self.payload['promo_code']

            db.add(order)
            db.commit()
            db.refresh(order)

        return order

    @abstractmethod
    def add_item(self):
        pass
