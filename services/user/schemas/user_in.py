from typing import Union
from datetime import datetime

from . import BaseUser


class UserInSchema(BaseUser):
    """ User in schema """
    phone: str
    email: Union[str, None] = None


    class Config:
        orm_mode = True