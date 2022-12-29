from fastapi import HTTPException, UploadFile, File
from starlette import status

from common import utils
from services.category.controllers import CategoryBaseController
from services.category.schemas.category_in import CategoryInSchema
from common.utils import PHOTO_TYPE


class CreateCategoryController(CategoryBaseController):
    def __init__(self, payload: dict):
        self.payload = payload
        super(CreateCategoryController, self).__init__()

    def execute(self):
        photo_sm = None
        photo_md = None
        try:
            slug = self._generate_slug(self.payload["name"])
            self.payload["slug"] = slug
            self.payload["active"] = True

            """ save photo """
            if self.payload["photo_sm"]:
                photo_sm = utils.save_photo(self.photo_path,
                             PHOTO_TYPE["category"],
                             self.payload["photo_sm"])
                self.payload["photo_sm"] = photo_sm

            if self.payload["photo_md"]:
                photo_md = utils.save_photo(self.photo_path,
                             PHOTO_TYPE["category"],
                             self.payload["photo_md"])
                self.payload["photo_md"] = photo_md

            """ save """
            new = self._create()

        except Exception as ex:
            #  logging
            utils.reject_photo(self.photo_path, PHOTO_TYPE["category"], photo_sm) if photo_sm else None
            utils.reject_photo(self.photo_path, PHOTO_TYPE["category"], photo_md) if photo_md else None
            #  logging
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category is not created: {ex.orig}",
            )

        return new



