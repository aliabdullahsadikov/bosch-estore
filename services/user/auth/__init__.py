from fastapi.security import OAuth2PasswordBearer
from uuid import UUID

from services.category.models.category import get_db
from services.user.models.user import User
# from services.user.schemas.sign_up import SignUpSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def current_user():
    with get_db() as db:
        user = db.query(User)\
            .filter(User.id == UUID('00d2b1e3-1f08-4f51-aad7-4bbe4927efe4'))\
            .first()
        return user
