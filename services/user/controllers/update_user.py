import uuid
from fastapi import HTTPException
from starlette import status

from services.user.controllers import BaseController
from services.user.models.user import User
from services.user.schemas import ResponseSchema
from services.user.schemas.user_in import UserInSchema
from services.user.schemas.user_out import UserOutSchema
from services.user.schemas.sign_up import SignUpSchema


class UpdateUserController(BaseController):

    def __init__(self, user_id: str, user_data: UserInSchema):
        """
        For update user operation
        :param user_data:
        """
        self.id = user_id
        self.request_body = user_data.dict()
        super(UpdateUserController, self).__init__()

    def execute(self):
        """ Get user """
        user = self.get_user_by_id()
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found!")

        try:
            updated = self._user_update()
        except HTTPException as ex:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"User has not updated: {ex.detail}",
            )

        return UserOutSchema.from_orm(updated)
