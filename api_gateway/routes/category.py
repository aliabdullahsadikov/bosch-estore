from typing import Union, List

from fastapi import APIRouter, Request, UploadFile, Form, File

from common.database.redis import cache_up
from services.category.controllers.create import CreateCategoryController
from services.category.controllers.delete import DeleteCategoryController
from services.category.controllers.get import GetCategoryController
from services.category.controllers.get_all import GetAllCategoriesController
from services.category.controllers.update import UpdateCategoryController
from services.category.schemas.category_in import CategoryInSchema
from services.category.schemas.category_out import CategoryOutSchema

category_routes = APIRouter()


@category_routes.post("/categories")
def create_category(
        name: str = Form(),
        parent_id: int = Form(),
        photo_sm: UploadFile = None,
        photo_md: UploadFile = None
):
    """
    Create category function
    :param name:
    :param parent_id:
    :param photo_sm:
    :param photo_md:
    :return:
    """
    payload = {
        "name": name,
        "parent_id": parent_id,
        "photo_sm": photo_sm,
        "photo_md": photo_md
    }
    return CreateCategoryController(payload).execute()


@category_routes.get("/categories/{category_id}")
def get(category_id: int):
    """
    Get category by ID
    :param category_id:
    :return:
    """
    return GetCategoryController(category_id).execute()


@category_routes.post("/categories/{category_id}")
def delete(category_id: int):
    """
    Delete category
    :param category_id:
    :return:
    """
    return DeleteCategoryController(category_id).execute()


@category_routes.get("/categories")
def get_all():
    """
    Get category list as a nested
    :return:
    """
    return GetAllCategoriesController().execute()


@category_routes.patch("/categories/{category_id}")
def update(
        category_id: int,
        name: str = Form(...),
        parent_id: int = Form(...),
        photo_sm: UploadFile = None,
        photo_md: UploadFile = None,
        active: bool = None
):
    """
    Update category
    :param name:
    :param parent_id:
    :param photo_sm:
    :param photo_md:
    :param active:
    :return:
    """
    payload = {
        "name": name,
        "parent_id": parent_id,
        "photo_sm": photo_sm,
        "photo_md": photo_md,
        "active": active
    }
    return UpdateCategoryController(category_id, payload).execute()
