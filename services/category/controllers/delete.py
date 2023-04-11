from fastapi import HTTPException, UploadFile
from starlette import status

from common import utils
from common.get_db import get_db
from services.category.controllers import CategoryBaseController
from services.category.schemas.category_in import CategoryInSchema
from services.category.schemas.category_out import CategoryOutSchema


class DeleteCategoryController(CategoryBaseController):

    def __init__(self, id: int):
        self.id = id
        super(DeleteCategoryController, self).__init__()

    def execute(self):
        try:
            category = self._get_category_by_id()

            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Category not found!"
                )
            try:
                deleted = self._delete_category(category)

                if deleted:
                    filenames: list = [category.photo_sm, category.photo_md]
                    deleted_photos_from_dir = utils.delete_photo(
                        self.photo_path,
                        filenames=filenames)

            except Exception as ex:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Category or its photos has not deleted: {ex.orig}"
                )

        except Exception as ex:
            # logging point
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found!"
            )

        return status.HTTP_200_OK

    def _delete_category(self, category):
        with get_db() as db:
            if category:
                db.delete(category)
                db.commit()

        return True

