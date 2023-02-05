from fastapi.security import OAuth2PasswordBearer
from uuid import UUID

from services.category.models.category import get_db
from services.user.models.user import User
from services.user.schemas.sign_up import SignUpSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def current_user():
    with get_db() as db:
        user = db.query(User)\
            .filter(User.id == UUID('0b8d6c3d-ed05-4cfc-896a-f599289d86a6'))\
            .first()
        return user
