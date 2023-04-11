import datetime
from uuid import UUID

from sqlalchemy.orm import class_mapper

from common.database import Base
from common.get_db import get_db
from services.order.controllers import OrderBaseController
from services.order.models.order import Order
from services.order.models.transaction import Transaction
from services.order.modules.order.order_manager import OrderManager
from services.order.schemas.shipping import ShippingSchema
from services.payment.payme.config import PAYMENT_CODE_PAYME


class ShippingOrderController(OrderBaseController):

    def __init__(self, payload: ShippingSchema):
        self._payload = payload.dict()
        super(ShippingOrderController, self).__init__(self._payload)

    def execute(self):
        """ Update """
        order_manager = OrderManager()
        order_manager.object = self._payload["id"]
        order_manager.update(**self._payload)

        """ Create Transaction """
        transaction = self.create_transaction(order_manager.object)

        return self.response(
            data={
                "amount": order_manager.object.total_price,
                "user_id": str(self.user.id)
            }
        )

    def create_transaction(self, order: Order):
        with get_db() as db:
            new_transaction = Transaction(
                user_id=self.user.id,
                order_id=order.id,
                payment_code=PAYMENT_CODE_PAYME,
                order_data=self.model_to_dict(order)
            )
            db.add(new_transaction)
            db.commit()
            db.refresh(new_transaction)

        return new_transaction

    def model_to_dict(self, model: Base):
        mapper = class_mapper(model.__class__)

        columns = [column.key for column in mapper.columns]

        values = {
            column: getattr(model, column).hex
            if isinstance(getattr(model, column), UUID)
            else getattr(model, column)
            for column in columns
        }
        if values.get("created_at"):
            values["created_at"] = str(values["created_at"])
        if values.get("updated_at"):
            values["updated_at"] = str(values["updated_at"])

        return values
