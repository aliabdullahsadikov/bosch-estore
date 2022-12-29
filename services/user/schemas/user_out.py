from typing import Union
from datetime import datetime

from . import BaseUser


class UserOutSchema(BaseUser):
    """ User out schema """
    phone: int
    status: int
    email: Union[str, None] = None
    created_at: datetime

    class Config:
        orm_mode = True