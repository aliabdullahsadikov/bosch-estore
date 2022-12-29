from starlette import status
from pydantic import BaseModel


class BaseResponseSchema(BaseModel):
    status: int = status.HTTP_200_OK
    success: str = "OK"
    message: str = "Success!"
    data: dict[str, None] = {}
