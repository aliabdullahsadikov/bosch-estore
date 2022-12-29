from datetime import datetime

from fastapi import HTTPException
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

# from common.database import database
from common.config import USER_STATUS
from common.database import get_db
from services.user.models.user import User
from services.user.schemas import ResponseSchema
from services.user.schemas.create import CreateSchema
from services.user.schemas.user_out import UserOutSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class BaseController(object):

    request_body = {}
    phone = ''
    id = ''

    def __init__(self):
        self.model = User

    def _user_exist_by_phone(self) -> bool:
        """ Check out user identity """
        phone = self.request_body["phone"] if self.request_body else self.phone
        with get_db() as db:
            user = db.query(self.model).filter(self.model.phone == phone).first()

        return True if user else False

    def _user_exist_by_id(self) -> bool:
        """ Check out user by id identity """
        with get_db() as db:
            user = db.query(self.model).filter(self.model.id == self.id).first()

        return True if user else False

    def _create(self, model: CreateSchema):
        """ Create user by sign up function """
        with get_db() as db:
            new_user = self.model(**model.dict())
            db.add(new_user)
            db.commit()
            db.refresh(new_user)

        return new_user

    def _user_update(self) -> User:
        """ Update user """
        updated = datetime.now()
        password = 'hfdkfdjslkfjwovjdkvjlksj'
        with get_db() as db:
            # user = db.query(self.model).update(**self.request_body) \
            #     .filter(self.model.id == self.id)
            user = self.model(password_hash=password, updated_at=password, **self.request_body)
            db.add(user)
            db.commit()
        return user

    def get_user_by_id(self) -> User:
        """ Get user by id """
        with get_db() as db:
            user = db.query(self.model).filter(self.model.id == self.id).first()
        return user

    def get_user_by_phone(self) -> User:
        """ Get user by id """
        with get_db() as db:
            user = db.query(self.model).filter(self.model.id == self.phone).first()
        return user

    def get_user_list(self, all, skip, limit):
        """ Get user list """
        with get_db() as db:
            if all:
                user = db.query(self.model)\
                    .offset(skip)\
                    .limit(limit)\
                    .all()
            else:
                user = db.query(self.model)\
                    .filter(self.model.status == USER_STATUS["active"])\
                    .offset(skip)\
                    .limit(limit)\
                    .all()
        return user

    @staticmethod
    def verify_password(password: str, hashed_password: str):
        return pwd_context.verify(password, hashed_password)

    @staticmethod
    def get_password_hash(password: str):
        return pwd_context.hash(password)
