from typing import Union, Text

from fastapi import UploadFile, Form
from pydantic import BaseModel, Field


class ProductBaseSchema(BaseModel):
    name: str = Form(default="lili", max_length=100, title="Product name")
    long_name: str = Form(default=None, title="Product long name")
    model: str = Form(default=None, title="Product model")
    manufacturer: str = Form(default=None, title="Product manufacturer")
    description_uz: Text = None
    description_ru: Text = None
    description_en: Text = None
    content_uz: Text = None
    content_ru: Text = None
    content_en: Text = None
    info_uz: Text = None
    info_ru: Text = None
    info_en: Text = None
