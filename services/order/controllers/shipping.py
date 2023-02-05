from services.order.controllers import OrderBaseController


class ShippingOrderController(OrderBaseController):

    def __init__(self, payload: ShippingSchema):
        self._payload = payload.dict()
        super(ShippingOrderController, self).__init__(self._payload)


