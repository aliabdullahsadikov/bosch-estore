from fastapi import APIRouter

from services.order.controllers.checkout import CheckoutOrderController
from services.order.controllers.shipping import ShippingOrderController
from services.order.schemas.checkout import CheckoutSchema
from services.order.schemas.shipping import ShippingSchema

order_routes = APIRouter()


@order_routes.post("/checkout")
def checkout(payload: CheckoutSchema):
    """
    Create Order
    :param payload
    :return:
    """
    return CheckoutOrderController(payload).execute()


@order_routes.post("/shipping")
def shipping(payload: ShippingSchema):
    """
    Save Shipping info
    :param payload
    :return:
    """
    return ShippingOrderController(payload).execute()
