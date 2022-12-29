import datetime
import pickle
from typing import List

from fastapi import HTTPException, UploadFile, File
from starlette import status

from common import utils
from common.utils import PHOTO_TYPE
from services.product.controllers import ProductBaseController


class GetProductController(ProductBaseController):
    def __init__(self, product_id: int):
        self.id = product_id
        super(GetProductController, self).__init__()

    def execute(self):
        try:

            product = self._get_product_by_id()
            # product = self._decod_text_fields(product)

        except Exception as ex:
            #  logging
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred while retrieve product: {ex}",
            )

        return product



