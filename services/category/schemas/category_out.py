from typing import Union

from fastapi import UploadFile
from pydantic import BaseModel, Field


class CategoryOutSchema(BaseModel):
    id: int
    name: str
    parent_id: int
    slug: str
    photo_sm: str
    photo_md: str
    # children: []

    class Config:
        orm_mode = True