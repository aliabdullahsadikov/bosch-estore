from fastapi import HTTPException
from starlette import status

from services.user.controllers import BaseController
from services.user.models.user import User
from services.user.schemas import ResponseSchema
from services.user.schemas.sign_up import SignUpSchema


class SignInController(BaseController):

    def __init__(self, request_body: SignInSchema):
        """
        For user sign in operation
        :param request_body:
        """
        self.request_body = request_body.dict()
        super(SignInController, self).__init__()


    def execute(self):
        """ check out: user already exist """
        user: User = self.get_user_by_phone()
        if not user:
            raise HTTPException(status.HTTP_302_FOUND, detail="User already exist!")

        check_pass = self.verify_password(self.request_body.password, user.password_hash)

        # login qilish kere

        return create
