from fastapi import HTTPException, UploadFile
from starlette import status

from common.database.redis import cache_up
from services.category.controllers import CategoryBaseController
from services.category.schemas.category_in import CategoryInSchema
from services.category.schemas.category_out import CategoryOutSchema


class GetAllCategoriesController(CategoryBaseController):

    def __init__(self):
        super(GetAllCategoriesController, self).__init__()

    def execute(self):
        try:

            categories = self.get_all_categories()

            if not categories:
                raise HTTPException(
                    status_code=status.HTTP_204_NO_CONTENT,
                    detail="There doesn't exist any category!"
                )

        except Exception as ex:
            # logging point
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error occurred in getting all categories: {ex}"
            )

        return categories



