from fastapi import HTTPException, UploadFile
from starlette import status

from services.category.controllers import CategoryBaseController
from services.category.schemas.category_in import CategoryInSchema
from services.category.schemas.category_out import CategoryOutSchema


class GetCategoryController(CategoryBaseController):

    def __init__(self, id: int):
        self.id = id
        super(GetCategoryController, self).__init__()

    def execute(self):
        try:
            category = self._get_category_by_id()

            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Category not found!"
                )
            category_out = CategoryOutSchema.from_orm(category)

        except Exception as ex:
            # logging point
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found!"
            )

        return category_out



