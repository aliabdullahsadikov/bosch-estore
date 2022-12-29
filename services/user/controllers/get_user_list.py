from fastapi import HTTPException
from starlette import status

from services.user.controllers import BaseController
from services.user.models.user import User
from services.user.schemas import ResponseSchema
from services.user.schemas.user_out import UserOutSchema
from services.user.schemas.sign_up import SignUpSchema


class GetUserListController(BaseController):

    def __init__(self, all: bool, skip: int = 0, limit: int = 100):
        """
        For get user list operation
        :param request_body:
        """
        self.all = all
        self.skip = skip
        self.limit = limit
        super(GetUserListController, self).__init__()

    def execute(self):
        """ Get user """
        user_list = self.get_user_list(self.all, self.skip, self.limit)
        if not user_list:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found!")

        out_list = []
        for user in user_list:
            out_list.append(UserOutSchema.from_orm(user))

        return out_list
