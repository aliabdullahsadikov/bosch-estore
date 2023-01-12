from fastapi import HTTPException
from starlette import status

from services.cart.controllers import CartBaseController, UserCartManager


class AddProductController(CartBaseController):

    def __init__(self, product_id: int):
        self.product_id = product_id
        super(AddProductController, self).__init__()

    def execute(self):
        product = self._get_product_by_id()

        if not product:
            self.logger.exception(f"Product not found: by ID - {self.product_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product not found: by ID - {self.product_id}"
            )

        result = {}
        try:
            cart_manager = UserCartManager()
            if cart_manager.active_cart:
                if cart_manager.has_item(self.product_id):
                    result = cart_manager.add(self.product_id)
                else:
                    result = cart_manager.create_item(product)
            else:
                cart_manager.create_cart(product)
        except HTTPException as exp:
            self.logger.exception(f"Error occurred in time to add item in cart: {exp.detail}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred in time to add item in cart: {exp.detail}"
            )
        # finally:
        #     self.logger.info(result)

        return status.HTTP_200_OK

