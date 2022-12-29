from fastapi.security import OAuth2PasswordBearer

from services.user.schemas.sign_up import SignUpSchema
from services.user.auth import oauth2_scheme

oauth2_scheme = oauth2_scheme
