from common.database import get_db
from services.product.models.product import Product


class ProductManager:

    def __init__(self, product_id):
        self._model = Product
        self._product = self._get_product_by_id(product_id)

    def _get_product_by_id(self, product_id):
        with get_db() as db:
            product = db.query(self._model).get(product_id)
            product.photos = product.photos

        return product
