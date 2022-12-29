import datetime

from fastapi import HTTPException, UploadFile, File
from starlette import status

from common import utils
from services.category.controllers import CategoryBaseController
from services.category.schemas.category_in import CategoryInSchema
from common.utils import PHOTO_TYPE


class UpdateCategoryController(CategoryBaseController):
    def __init__(self, id: int, payload: dict):
        self.id = id
        self.payload = payload
        super(UpdateCategoryController, self).__init__()

    def execute(self):
        photo_sm = None
        photo_md = None

        category = self._get_category_by_id()

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category has not found by target ID: {self.payload['id']}"
            )

        try:
            if category.name != self.payload["name"]:
                slug = self._generate_slug(self.payload["name"])
            else:
                slug = category.slug

            self.payload["slug"] = slug
            self.payload["active"] = category.active\
                if category.active == self.payload["active"]\
                else self.payload["active"]

            """ save photo """
            """ photo_sm """
            if not self.payload["photo_sm"]:
                self.payload["photo_sm"] = category.photo_sm
            else:
                photo_sm = utils.save_photo(
                    self.photo_path,
                    PHOTO_TYPE["category"],
                    self.payload["photo_sm"]
                )
                self.payload["photo_sm"] = photo_sm

            """ photo_md """
            if not self.payload["photo_md"]:
                self.payload["photo_md"] = category.photo_md
            else:
                photo_md = utils.save_photo(
                    self.photo_path,
                    PHOTO_TYPE["category"],
                    self.payload["photo_md"]
                )
                self.payload["photo_md"] = photo_md

            """ update """
            updated = self._update()

        except Exception as ex:
            #  logging
            utils.reject_photo(self.photo_path, PHOTO_TYPE["category"], photo_sm) if photo_sm else None
            utils.reject_photo(self.photo_path, PHOTO_TYPE["category"], photo_md) if photo_md else None
            #  logging
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category is not created: {ex.orig}",
            )

        return updated



