from fastapi import APIRouter

from services.cart.controllers.add import AddProductController
from services.cart.controllers.reduce import ReduceItemController
from services.cart.controllers.remove_cart import RemoveCartController
from services.cart.controllers.remove_item import RemoveProductController

cart_routes = APIRouter()


@cart_routes.get("/cart/add/{product_id}")
def add(product_id: int):
    """
    Add a product to cart
    :param product_id
    :return:
    """
    return AddProductController(product_id).execute()


@cart_routes.get("/cart/reduce/{product_id}")
def reduce(product_id: int):
    """
    Remove a cart
    """
    return ReduceItemController(product_id).execute()


@cart_routes.get("/cart/remove_item/{product_id}")
def remove_item(product_id: int):
    """
    Remove a product to cart
    :param product_id
    :return:
    """
    return RemoveProductController(product_id).execute()


@cart_routes.post("/cart/remove_cart")
def remove_cart():
    """
    Remove a cart
    """
    return RemoveCartController().execute()
