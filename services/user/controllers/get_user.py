from fastapi import HTTPException
from starlette import status

from services.user.controllers import BaseController
from services.user.models.user import User
from services.user.schemas import ResponseSchema
from services.user.schemas.user_out import UserOutSchema
from services.user.schemas.sign_up import SignUpSchema


class GetUserController(BaseController):

    def __init__(self, id: str):
        """
        For get user operation
        :param user_id:
        """
        self.id = id
        super(GetUserController, self).__init__()

    def execute(self):
        """ Get user """
        user = self.get_user_by_id()
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found!")

        return UserOutSchema.from_orm(user)
