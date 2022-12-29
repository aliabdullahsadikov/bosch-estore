import datetime
import pickle
from typing import List

from fastapi import HTTPException, UploadFile, File
from starlette import status

from common import utils
from common.database import get_db
from common.utils import PHOTO_TYPE
from services.category.models.category import Category, Category_Product
from services.product.controllers import ProductBaseController


class GetAllByCategoryController(ProductBaseController):
    def __init__(self, category_id: int):
        self.category_id = category_id
        super(GetAllByCategoryController, self).__init__()

    def execute(self):
        try:
            category = self._get_category(self.category_id)
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Category not found: by this ID {self.category_id}"
                )

            product_ids = self._get_product_ids(self.category_id)

            # product = self._get_product_by_id()
            # product = self._decod_text_fields(product)

        except Exception as ex:
            #  logging
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while retrieve product: {ex}",
            )

        return None

    def _get_category(self, category_id):
        with get_db() as db:
            model = db.query(Category).get(category_id)
            model = model

        return model

    def _get_product_ids(self, category_id):
        with get_db() as db:
            product_ids = db.query(Category_Product.product_id)\
                .filter(Category_Product.category_id == category_id)\
                .all()

        return product_ids