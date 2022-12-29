from pydantic import BaseModel, Field
from . import BaseUser


class SignUpSchema(BaseModel):
    phone: str
    password: str
