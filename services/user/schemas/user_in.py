from typing import Union, Optional
from datetime import datetime

from . import BaseUser


class UserInSchema(BaseUser):
    """ User in schema """
    phone: Optional[str] = None
    email: Union[str, None] = None


    class Config:
        orm_mode = True