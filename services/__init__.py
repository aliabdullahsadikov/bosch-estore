from uuid import UUID

from pydantic import BaseModel
from starlette import status

from clients.mongo_client import MongoCoreClient
from common.database import get_db
from common.database.mongo import myclient, mdb
from logs.log_base import logging, file_error_handler, file_info_handler, console_handler
from services.user.models.user import User


class BaseController(object):

    def __init__(self):
        self.user = current_user()
        self.response = ResponseSchema

        """ 
        Logging option:
        If you want to add log handler you have to add below
        snippet into the target base class init def 
        """
        logger = logging.getLogger(self.__module__)
        logger.addHandler(file_error_handler)
        logger.addHandler(file_info_handler)
        logger.addHandler(console_handler)
        self.logger = logger
        """ end """

        self._mongo_client = MongoCoreClient(
            mongo_client=myclient,
            mongo_db=mdb,
            document=None
        )


class ResponseSchema(BaseModel):
    status_code: int = status.HTTP_200_OK
    message: str = "OK"
    error: bool = False
    data: dict = {}


def current_user():
    with get_db() as db:
        user = db.query(User)\
            .filter(User.id == UUID('0b8d6c3d-ed05-4cfc-896a-f599289d86a6'))\
            .first()
        return user
