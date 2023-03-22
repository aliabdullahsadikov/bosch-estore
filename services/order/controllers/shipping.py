from services.order.controllers import OrderBaseController
from services.order.modules.order.order_manager import OrderManager
from services.order.schemas.shipping import ShippingSchema


class ShippingOrderController(OrderBaseController):

    def __init__(self, payload: ShippingSchema):
        self._payload = payload.dict()
        super(ShippingOrderController, self).__init__(self._payload)

    def execute(self):
        order_manager = OrderManager()
        order_manager.object = self._payload["id"]
        order_manager.update(**self._payload)

        return self.response()
