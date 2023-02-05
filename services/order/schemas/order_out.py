from typing import Any, Text, List

from pydantic import BaseModel

from services.order.schemas import OrderBase


class OrderItemOutSchema(BaseModel):
    order_id: int
    product_id: int
    product_name: str = None
    amount: int
    price: float = None
    sale_percent: int = None
    sale_price: float = None
    total_price: float = None

    class Config:
        orm_mode = True


class OrderOutSchema(OrderBase):
    sub_total: float = None
    total_price: float = None

    fio: str = None
    phone: str = None
    address: str = None
    company: str = None
    email: str = None
    description: Text = None

    shipping_type: Any = None
    shipping_comment: Text = None

    items: List[OrderItemOutSchema]

    class Config:
        orm_mode = True


