import datetime
from typing import List

from fastapi import HTTPException, UploadFile, File
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


class UpdateProductController(ProductBaseController):
    def __init__(self, product_id: int, payload: dict, category: int, photos: List[UploadFile]):
        self.id = product_id
        self.payload = payload
        self.category = category
        self.photos = photos
        super(UpdateProductController, self).__init__()

    def execute(self):

        product = self._get_product_by_id()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found!"
            )

        try:

            self.payload["updated_at"] = datetime.datetime.now()
            """ Update product """
            updated = self._update()

            if updated:
                """ update photos """

                if self.photos:  # new ones
                    """ Delete old photos if new ones arrived """

                    for photo in product.photos:  # old ones
                        """ Delete old photos """

                        try:
                            """ From files """
                            utils.reject_photo(self.photo_path, PHOTO_TYPE["product"], photo.photo_sm) if photo.photo_sm else None
                            utils.reject_photo(self.photo_path, PHOTO_TYPE["product"], photo.photo_md) if photo.photo_md else None
                            utils.reject_photo(self.photo_path, PHOTO_TYPE["product"], photo.photo_lg) if photo.photo_lg else None
                        except Exception as ex:
                            self.logger.exception(f"Exception message: {ex}")

                        """ From database """
                        self._delete_photos(photo)

                    for i in range(len(self.photos)):
                        """ resize and save new photos """
                        photo_sm, photo_md, photo_lg = self.accomplish(self.photos[i])
                        saved_photos = {
                                "sm": photo_sm,
                                "md": photo_md,
                                "lg": photo_lg
                            }

                        """ save model """
                        main = True if i == 0 else False
                        new_photo_model = self._create_product_photo(product, main, saved_photos)
                else:
                    if not product.photos:
                        self._save_default_photo(product)

                """ create the relation with the category """
                try:
                    category_product = self._update_category_product_relation()
                except Exception as ex:
                    self.logger.exception(f"Exception message: (Update product category in function update product) - {ex}")
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Relation is not created: {ex}",
                    )

        except Exception as ex:
            self.logger.exception(f"Exception message:  {ex}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product is not created: {ex}",
            )

        return self._get_product_by_id()

    def _update_category_product_relation(self):
        with get_db() as db:
            update = db.query(Category_Product)\
                .filter(Category_Product.product_id == self.id)\
                .update({"category_id":self.category})
            db.commit()

        return update

    def _save_default_photo(self, product):
        with get_db() as db:
            default = ProductPhoto(
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
