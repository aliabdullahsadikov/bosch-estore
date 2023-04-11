from pydantic import BaseModel


class ValidateCheckTransaction(BaseModel):
    id: int