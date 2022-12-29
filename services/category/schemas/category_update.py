from typing import Union

from fastapi import UploadFile
from pydantic import BaseModel, Field

from services.category.schemas.category_in import CategoryInSchema


class CategoryUpdateSchema(CategoryInSchema):
    # name: str = Field(..., max_length=100, title="Category name")
    # parent_id: int = Field(default=0, title="Category parent")
    active: bool = None