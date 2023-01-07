import array
import datetime
import pickle
from typing import List

from fastapi import HTTPException, UploadFile, File
from sqlalchemy import text
from starlette import status
from sqlalchemy.dialects.postgresql import array_agg

from common import utils
from common.database import get_db
from common.utils import PHOTO_TYPE
from services.category.models.category import Category, Category_Product
from services.product.controllers import ProductBaseController


class GetAllController(ProductBaseController):
    def __init__(self, category_id: int = None, limit: int = 30, page: int = None):
        self.category_id = category_id
        self.limit = limit,
        self.page = page
        super(GetAllController, self).__init__()

    def execute(self):
        try:
            product_ids = []
            if self.category_id:
                category = self._get_category(self.category_id)
                if not category:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Category not found: by this ID {self.category_id}"
                    )
                product_ids = self._get_product_ids(self.category_id)

            products = self._get_products(product_ids, active=True)

        except Exception as ex:
            # should be logging performance line
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while retrieve product: {ex}",
            )

        return products

    def _get_category(self, category_id):
        with get_db() as db:
            model = db.query(Category).get(category_id)
            model = model

        return model

    def _get_product_ids(self, category_id) -> list:
        """
        Product ids which related to category
        :param category_id:
        :return: list data
        """
        with get_db() as db:
            command = text(f"""
                SELECT product_id
                FROM category_product as cp
                WHERE cp.category_id = {category_id}
            """)
            sql_row = db.execute(command)
        data = [row.product_id for row in sql_row]

        return data
