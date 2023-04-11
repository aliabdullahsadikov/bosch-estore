from typing import Text, Any, Optional

from pydantic import BaseModel


class ShippingSchema(BaseModel):
    id: int
    shipping_type: int
    shipping_comment: Optional[Text] = None

    fio: Optional[str] = None
    phone: str = None
    address: str = None
    company: Optional[str] = None
    email: Optional[str] = None
    description: Optional[Text] = None

