from typing import Optional

from pydantic import BaseModel


class SuccessResponse(BaseModel):
    result: dict
    id: Optional[int] = None
