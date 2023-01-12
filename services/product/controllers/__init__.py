from typing import List

from logs.log_base import logging

from common.database import get_db
from services import BaseController
from services.product.models.product import Product
from services.product.models.product_photos import ProductPhoto

product_status = {
    "active": 1,
    "inactive": 0,
    "trash": -1
}


class ProductBaseController(BaseController):

    payload = {}
    id = None
    photo_path = "common/static/photo"

    def __init__(self):
        super(ProductBaseController, self).__init__()
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
            # products = db.query(self.model)\
            #     .filter(self.model.id.in_(product_ids))\
            #     .filter(self.model.status == product_status["active"]) \
            #     .limit(2)\
            #     .offset(1)\
            #     .all()

            if product_ids:
                """ The case for obtain products by category """
                products = products.filter(self.model.id.in_(product_ids))

            if active:
                """ receive only active ones """
                products = products.filter(self.model.status == product_status["active"])

            count = products.count() / self.limit[0]

            if self.page:
                """ pagination page """
                offset = (self.page - 1) * self.limit[0]
                products = products.offset(offset)

            products = products.limit(self.limit[0])

            products = products.all()

            data = []
            for row in products:
                row.photos = row.photos
                data.append(row)

            response = {
                "data": data,
                "pages": count,
                "limit": self.limit[0],
                "page": self.page
            }

        return response

    def _create(self):
        """ Create Product """
        with get_db() as db:
            new = self.model(**self.payload)
            db.add(new)
            db.commit()
            db.refresh(new)

        return new

    def _update(self):
        """ Update Product """
        with get_db() as db:
            target_model = db.query(self.model)\
                .filter(self.model.id == self.id)\
                .update(self.payload)
            db.commit()

        return target_model

    def _delete_photos(self, photo: ProductPhoto):
        with get_db() as db:
            db.delete(photo)
            db.commit()


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
