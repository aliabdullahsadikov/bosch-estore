from typing import List, Text

from fastapi import APIRouter, Request, UploadFile, Form, File
from pydantic import Field

from services.product.controllers.create import CreateProductController
from services.product.controllers.get import GetProductController
from services.product.controllers.get_all_by_category import GetAllController
from services.product.models.product import Product
from services.product.schemas.product_in import ProductInSchema

product_routes = APIRouter()


@product_routes.get("/products/{product_id}")
def get_by_id(product_id: int):
    return GetProductController(product_id).execute()


@product_routes.get("/products")
def get_all(category_id: int = None):
    return GetAllController(category_id).execute()


@product_routes.post("/products")
def create(
        name: str = Form(...),
        category: int = Form(...),
        long_name: str = None,
        model: str = None,
        manufacturer: str = None,
        description_uz: Text = None,
        description_ru: Text = None,
        description_en: Text = None,
        content_uz: Text = None,
        content_ru: Text = None,
        content_en: Text = None,
        info_uz: Text = None,
        info_ru: Text = None,
        info_en: Text = None,
        price: float = None,
        status: int = None,
        amount: int = None,
        tags: Text = None,
        photos: List[UploadFile] = File(description="Attach only files that file size is lower than 1MB!"),
):
    payload = ProductInSchema(
        name=name.capitalize(),
        long_name=long_name.capitalize(),
        model=model.upper(),
        manufacturer=manufacturer.capitalize(),
        description_uz=description_uz,
        description_ru = description_ru,
        description_en = description_en,
        content_uz = content_uz,
        content_ru = content_ru,
        content_en = content_en,
        info_uz = info_uz,
        info_ru = info_ru,
        info_en = info_en,
        price = price,
        status = status,
        amount = amount,
        tags = tags
    )


    return CreateProductController(payload.dict(), photos, category).execute()
