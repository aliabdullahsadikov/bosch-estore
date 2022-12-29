from fastapi import HTTPException
from starlette import status

from services.user.controllers import BaseController
from services.user.models.user import User
from services.user.schemas import ResponseSchema
from services.user.schemas.create import CreateSchema
from services.user.schemas.sign_up import SignUpSchema
from services.user.schemas.user_out import UserOutSchema


class SignUpController(BaseController):

    def __init__(self, request_body: SignUpSchema):
        """
        For user sign up operation
        :param request_body:
        """
        self.request_body = request_body.dict()
        super(SignUpController, self).__init__()

    def execute(self):
        """ check out: user already exist """
        if self._user_exist_by_phone():
            raise HTTPException(status.HTTP_302_FOUND, detail="User already exist!")

        try:
            model = CreateSchema(
                phone=self.request_body['phone'],
                password_hash=self.get_password_hash(self.request_body['password']),
                otp_secret=1234,  # not implemented
                email=self.request_body.get("email")
            )

            """ create """
            created = self._create(model)

        except HTTPException as ex:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"User not created: {ex.detail}"
            )

        return UserOutSchema.from_orm(created)
