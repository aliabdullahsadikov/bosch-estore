from clients.mongo_client import MongoCoreClient
from common.database import get_db
from common.database.mongo import myclient, mdb
from services import BaseController
from services.cart.models.cart import Cart
from services.order.models.order import Order
from services.order.schemas.checkout import CartDataSchema


class OrderBaseController(BaseController):

    def __init__(self, payload):
        self._model = Order
        super(OrderBaseController, self).__init__()
        self.payload = payload
        self._mongo_client = MongoCoreClient(
            mongo_client=myclient,
            mongo_db=mdb,
            document=None
        )


    def active_sale(self):
        return None

    def create_order(self, cart: CartDataSchema):
        """
        Method will receive cart as a mongo object
        :param cart:
        :return:
        """
        with get_db() as db:
            order = self._model()
            order.cart_id = str(cart.cart_id)
            order.user_id = self.user.id
            order.promo_code = self.payload['promo_code']

            db.add(order)
            db.commit()
            db.refresh(order)

        return order

    def valid_promo(self):
        """
        Check promo code if is this exists in db than return True
        :return:
        """
        return True

    def order_exist(self, cart: CartDataSchema):
        with get_db() as db:
            order = db.query(Order).filter(Order.cart_id == cart.cart_id).first()

        return True if order else False


"""
steps:
1 checkout
2 shipping
3 payment

"""