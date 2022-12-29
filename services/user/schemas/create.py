from typing import Union

from . import BaseUser


class CreateSchema(BaseUser):
    """ User create schema """
    phone: int
    password_hash: str
    otp_secret: int
    email: Union[str, None] = None

    class Config:
        orm_mode = True