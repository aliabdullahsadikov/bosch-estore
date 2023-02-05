from fastapi import APIRouter

from services.order.controllers.checkout import CheckoutOrderController
from services.order.schemas.checkout import CheckoutSchema

order_routes = APIRouter()


@order_routes.post("/checkout")
def checkout(payload: CheckoutSchema):
    """
    Create Order
    :param payload
    :return:
    """
    return CheckoutOrderController(payload).execute()
