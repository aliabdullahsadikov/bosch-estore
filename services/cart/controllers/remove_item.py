from fastapi import HTTPException
from starlette import status

from services.cart.controllers import CartBaseController, UserCartManager


class RemoveProductController(CartBaseController):

    def __init__(self, product_id: int):
        self.product_id = product_id
        super(RemoveProductController, self).__init__()

    def execute(self):
        product = self._get_product_by_id()

        if not product:
            self.logger.exception(f"Product not found: by ID - {self.product_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product not found: by ID - {self.product_id}"
            )

        try:
            cart_manager = UserCartManager()
            if cart_manager.active_cart:
                if cart_manager.has_item(self.product_id):
                    cart_manager.remove_item(self.product_id)
                else:
                    self.logger.error(
                        "Item not found: In remove function occurred error due to has not fount target item"
                    )
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Item not found:"
                    )
        except HTTPException as exp:
            self.logger.exception(f"Error occurred in time to remove item in cart: {exp.detail}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error occurred in time to remove item in cart: {exp.detail}"
            )

        return status.HTTP_200_OK

