from typing import Any, Text, List

from pydantic import BaseModel

from services.order.schemas import OrderBase


class OrderItemInSchema(BaseModel):
    order_id: int
    product_id: int
    amount: int
    price: float = None
    sale_percent: int = None
    sale_price: float = None
    # total_price: float = None


class OrderInSchema(OrderBase):
    sub_total: float
    total_price: float

    fio: str
    phone: str
    address: str
    company: str
    email: str
    description: Text

    shipping_type: Any
    shipping_comment: Text



