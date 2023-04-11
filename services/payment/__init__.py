from common.get_db import get_db
from services.order.models.order import Order


class BasePayment:
    def __init__(self):
        pass

    def get_order(self, order_id) -> Order:
        with get_db() as db:
            order = db.query(Order).filter(Order.id == order_id).first()
            db.commit()
            return order
