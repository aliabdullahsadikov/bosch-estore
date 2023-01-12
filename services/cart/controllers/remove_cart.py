from fastapi import HTTPException
from starlette import status

from services.cart.controllers import CartBaseController, UserCartManager


class RemoveCartController(CartBaseController):

    def __init__(self):
        super(RemoveCartController, self).__init__()

    def execute(self):
        try:
            cart_manager = UserCartManager()
            if cart_manager.active_cart:
                cart_manager.remove_cart()
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

