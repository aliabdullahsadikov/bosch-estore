from pydantic import BaseModel


class Error(BaseModel):
    code: int
    message: dict
    data: str = None


class ErrorResponse(BaseModel):
    error: Error
    id: int


