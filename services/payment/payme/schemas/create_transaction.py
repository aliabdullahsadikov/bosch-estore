from pydantic import BaseModel


# class Account(BaseModel):
#     phone: str
#     order_id: int


class ValidatorCreateTransaction(BaseModel):
    id: str
    time: int
    amount: int
    account: dict
