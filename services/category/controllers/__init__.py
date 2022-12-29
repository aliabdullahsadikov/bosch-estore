import datetime

from fastapi import UploadFile, HTTPException
from starlette import status

from common.database import get_db
from common.database.redis import cache_up
from services.category.models.category import Category


class CategoryBaseController(object):

    payload = {}
    id = None
    photo_path = "common/static/photo"

    def __init__(self):
        self.model = Category

    def _create(self):
        """ Create Category """
        with get_db() as db:
            new = self.model(**self.payload)
            db.add(new)
            db.commit()
            db.refresh(new)

        return new

    def _update(self):
        """ Update Category """
        with get_db() as db:
            target_model = db.query(self.model).get(self.id)
            target_model.name = self.payload["name"]
            target_model.parent_id = self.payload["parent_id"]
            target_model.slug = self.payload["slug"]
            target_model.active = self.payload["active"]
            target_model.photo_sm = self.payload["photo_sm"]
            target_model.photo_md = self.payload["photo_md"]
            target_model.updated_at = datetime.datetime.now()
            db.commit()
            db.refresh(target_model)

        return target_model

    @staticmethod
    def _generate_slug(name: str) -> str:
        """ Generate slug """
        name = name.strip()
        name = name.lower()
        return name.replace(" ", "_")

    def _get_category_by_id(self):
        """ Get category by ID """
        with get_db() as db:
            category = db.query(self.model).get(self.id)

        return category

    @staticmethod
    @cache_up
    def get_all_categories():
        """ Get all categories """
        with get_db() as db:
            categories = db.query(Category)\
                .filter(Category.active, Category.parent_id == 0)\
                .all()

        """ generate category tree """
        for category in categories:
            children = category()

        return categories
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
