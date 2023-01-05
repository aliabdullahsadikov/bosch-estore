import datetime
import pickle

from fastapi import UploadFile, HTTPException
from starlette import status

from common import utils
from common.database import get_db
from common.database.redis import cache_up
from services.product.models.product import Product

product_status = {
    "active": 1,
    "inactive": 0,
    "trash": -1
}

class ProductBaseController(object):

    payload = {}
    id = None
    photo_path = "common/static/photo"

    def __init__(self):
        self.model = Product

    def _get_products(self, product_ids: list = [], active: bool = None) -> Product:
        """
        The function responsible for receive products
        :param product_ids: Receive category related
        :param active:
        :return: Product
        """
        with get_db() as db:
            products = db.query(self.model)
            if product_ids:
                """ The case for obtain products by category """
                products.filter(self.model.id in product_ids)

            if active:
                """ receive only active ones """
                products.filter(self.model.status == product_status["active"])

            products.all()

            data = []
            for row in products:
                row.photos = row.photos
                data.append(row)

        return data

    def _create(self):
        """ Create Product """
        with get_db() as db:
            new = self.model(**self.payload)
            db.add(new)
            db.commit()
            db.refresh(new)

        return new

    # def _update(self):
    #     """ Update Category """
    #     with get_db() as db:
    #         target_model = db.query(self.model).get(self.id)
    #         target_model.name = self.payload["name"]
    #         target_model.parent_id = self.payload["parent_id"]
    #         target_model.slug = self.payload["slug"]
    #         target_model.active = self.payload["active"]
    #         target_model.photo_sm = self.payload["photo_sm"]
    #         target_model.photo_md = self.payload["photo_md"]
    #         target_model.updated_at = datetime.datetime.now()
    #         db.commit()
    #         db.refresh(target_model)
    #
    #     return target_model
    #
    # @staticmethod
    # def _generate_slug(name: str) -> str:
    #     """ Generate slug """
    #     name = name.strip()
    #     name = name.lower()
    #     return name.replace(" ", "_")
    #
    def _get_product_by_id(self):
        """ Get product by ID """
        with get_db() as db:
            product = db.query(self.model).get(self.id)
            product.photos = product.photos

        return product

    @staticmethod
    def _decod_text_fields(product: Product) -> Product:
        """
        All text fields saved with a pickle dumps function in order to encode,
        and when we want to retrieve this object we must get by pickle loads in order to
        decode.
        :param product:
        :return:
        """
        import base64

        # product.description_uz = base64.b64encode(product.description_uz)
        # product.description_ru = pickle.loads(product.description_ru)
        # product.description_en = pickle.loads(product.description_en)
        #
        # product.content_uz = pickle.loads(product.content_uz)
        # product.content_ru = pickle.loads(product.content_ru)
        # product.content_en = pickle.loads(product.content_en)
        #
        # product.info_uz = pickle.loads(product.info_uz)
        # product.info_ru = pickle.loads(product.info_ru)
        # product.info_en = pickle.loads(product.info_en)

        return product

    # @staticmethod
    # @cache_up
    # def get_all_categories():
    #     """ Get all categories """
    #     with get_db() as db:
    #         categories = db.query(Category)\
    #             .filter(Category.active, Category.parent_id == 0)\
    #             .all()
    #
    #     """ generate category tree """
    #     for category in categories:
    #         children = category()
    #
    #     return categories
    #
    # @staticmethod
    # def get_children(category):
    #     with get_db() as db:
    #         child_categories = db.query(Category)\
    #             .filter(Category.parent_id == category.id, Category.active)\
    #             .all()
    #
    #     if not child_categories:
    #         return None
    #     pass
    #
    # @staticmethod
    # def get_category_by_parent_id(parent_id):
    #
