from typing import Union
from starlette import status

from pydantic import BaseModel

from api_gateway.schemas import BaseResponseSchema


class BaseUser(BaseModel):
    firstname: Union[str, None] = "unnamed"
    lastname: Union[str, None] = None

    class Config:
        orm_mode = True


class ResponseSchema(BaseModel):
    status: int = status.HTTP_200_OK
    success: bool = True
    message: str = "Success!"
    data: dict = {}
