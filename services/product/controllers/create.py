import datetime
import pickle
from typing import List

from fastapi import HTTPException, UploadFile, File
from sqlalchemy import insert
from starlette import status

from common import utils
from common.config import DEVELOPMENT_CONFIGS
from common.get_db import get_db
from common.database import Base
from common.image_lib.product_image_manager import ProductImgManager, PHOTO_SIZE
from common.utils import PHOTO_TYPE
from services.category.models.category import Category_Product
from services.product.controllers import ProductBaseController
from services.product.models.product import Product
from services.product.models.product_photos import ProductPhoto

img_conf = DEVELOPMENT_CONFIGS["image_conf"]


class CreateProductController(ProductBaseController):
    def __init__(self, payload: dict, photos: List, category: int):
        self.category = category
        self.payload = payload
        self.photos = photos
        super(CreateProductController, self).__init__()

    def execute(self):
        try:
            self.payload["created_at"] = datetime.datetime.now()

            new = self._create()

            if new:
                """ save photo """
                if self.photos:
                    for i in range(len(self.photos)):
                        """ resize and save photos """
                        photo_sm, photo_md, photo_lg = self.accomplish(self.photos[i])
                        saved_photos = {
                                "sm": photo_sm,
                                "md": photo_md,
                                "lg": photo_lg
                            }

                        """ save model """
                        main = True if i == 0 else False
                        new_photo_model = self._create_product_photo(new, main, saved_photos)
                else:
                    self._save_default_photo(new)

                """ create the relation with the category """
                try:
                    category_product = self._create_category_product_model(new.id, self.category)
                except Exception as ex:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Relation is not created: {ex}",
                    )

        except Exception as ex:
            #  logging
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category is not created: {ex}",
            )

        return new

    def _create_category_product_model(self, product_id, category_id):
        with get_db() as db:
            new_relation = Category_Product(product_id=product_id, category_id=category_id)
            db.add(new_relation)
            db.commit()
            db.refresh(new_relation)

        return new_relation

    def _save_default_photo(self, product):
        with get_db() as db:
            default = self.model(
                product_id=product.id,
                main=True,
                active=True,
                photo_sm=img_conf["default_images"]["product"]["sm"],
                photo_md=img_conf["default_images"]["product"]["md"],
                photo_lg=img_conf["default_images"]["product"]["lg"]
            )
            db.add(default)
            db.commit()
            db.refresh(default)

        return default

    def _create_product_photo(self, product: Product, main: bool, photo_path: dict):
        with get_db() as db:
            product_photo = ProductPhoto(
                product_id=product.id,
                main=main,
                active=True,
                photo_sm=photo_path["sm"],
                photo_md=photo_path["md"],
                photo_lg=photo_path["lg"]
            )
            db.add(product_photo)
            db.commit()
            db.refresh(product_photo)

        return product_photo

    def accomplish(self, photo):
        sm = ''
        md = ''
        lg = ''
        photo_sm = ProductImgManager(photo, PHOTO_SIZE["sm"])
        try:
            sm = photo_sm.save()
        except Exception as ex:
            photo_sm.reject()
            photo_sm = ""

        photo_md = ProductImgManager(photo, PHOTO_SIZE["md"])
        try:
            md = photo_md.save()
        except Exception as ex:
            photo_md.reject()
            photo_md = ""

        photo_lg = ProductImgManager(photo, PHOTO_SIZE["lg"])
        try:
            lg = photo_lg.save()
        except Exception as ex:
            photo_lg.reject()
            photo_lg = ""

        return sm, md, lg

# self.payload['description_uz'] = base64.b64encode(self.payload['description_uz'].encode("utf-8"))
# self.payload['description_ru'] = pickle.dumps(self.payload['description_ru'])
# self.payload['description_en'] = pickle.dumps(self.payload['description_en'])
#
# self.payload['content_uz'] = pickle.dumps(self.payload['content_uz'])
# self.payload['content_ru'] = pickle.dumps(self.payload['content_ru'])
# self.payload['content_en'] = pickle.dumps(self.payload['content_en'])
#
# self.payload['info_uz'] = pickle.dumps(self.payload['info_uz'])
# self.payload['info_ru'] = pickle.dumps(self.payload['info_ru'])
# self.payload['info_en'] = pickle.dumps(self.payload['info_en'])

