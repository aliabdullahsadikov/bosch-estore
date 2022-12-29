import uuid
from typing import List

from fastapi import APIRouter, Request, Depends
from starlette import status

from services.user.controllers.get_user import GetUserController
from services.user.controllers.get_user_list import GetUserListController
from services.user.controllers.sign_up import SignUpController
from services.user.controllers.update_user import UpdateUserController
from services.user.schemas import ResponseSchema
from services.user.schemas.sign_up import SignUpSchema
from api_gateway.security import oauth2_scheme
from services.user.schemas.user_in import UserInSchema
from services.user.schemas.user_out import UserOutSchema

user_routes = APIRouter()


# token: str = Depends(oauth2_scheme),  // this code snipped for enabling token authorization
@user_routes.post("/users", response_model=UserOutSchema, status_code=status.HTTP_201_CREATED)
def sign_up(payload: SignUpSchema):
    return SignUpController(payload).execute()


@user_routes.get("/users/{user_id}", response_model=UserOutSchema, status_code=status.HTTP_200_OK)
def get_user(user_id: str):
    return GetUserController(user_id).execute()


@user_routes.get("/users", response_model=List[UserOutSchema], status_code=status.HTTP_200_OK)
def get_users(all_users: bool = None, skip: int = 0, limit: int = 100):
    return GetUserListController(all_users, skip=skip, limit=limit).execute()


@user_routes.patch("/users/{user_id}", response_model=UserOutSchema, status_code=status.HTTP_200_OK)
def update_user(user_id: str, payload: UserInSchema):
    return UpdateUserController(user_id, payload).execute()
