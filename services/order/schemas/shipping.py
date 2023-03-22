from typing import Text, Any

from pydantic import BaseModel


class ShippingSchema(BaseModel):
    id: int
    shipping_type: Any
    shipping_comment: Text = None

    fio: str = None
    phone: str = None
    address: str = None
    company: str = None
    email: str = None
    description: Text = None

