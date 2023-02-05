from typing import List

from bson import ObjectId
from pydantic import BaseModel
from starlette import status


class CartItemInSchema(BaseModel):
    product_id: int
    amount: int


class CheckoutSchema(BaseModel):
    cart_id: str
    promo_code: str
    items: List[CartItemInSchema]


class CartDataSchema(BaseModel):
    cart_id: str
    cart_data: dict
    items: List[CartItemInSchema]