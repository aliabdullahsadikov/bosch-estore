from typing import Union, Text

from fastapi import UploadFile, Form
from pydantic import Field

from services.product.schemas.base import ProductBaseSchema


class ProductInSchema(ProductBaseSchema):
    price: float = Form(default=1.0, gt=1.0)
    status: int = Form(default=1)
    amount: int = Form(default="lolo")
    tags: Text = None

    class Config:
        orm_mode = True
