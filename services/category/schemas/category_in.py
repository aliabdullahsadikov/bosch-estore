from typing import Union

from fastapi import UploadFile
from pydantic import BaseModel, Field


class CategoryInSchema(BaseModel):
    # name: str = Field(..., max_length=100, title="Category name")
    # parent_id: int = Field(default=0, title="Category parent")
    name: str
    parent_id: int