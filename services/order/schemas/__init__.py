from pydantic import BaseModel, UUID4


class OrderBase(BaseModel):
    user_id: UUID4
    cart_id: str
    status: int
