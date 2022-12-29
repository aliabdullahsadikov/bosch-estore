from fastapi.security import OAuth2PasswordBearer

from services.user.schemas.sign_up import SignUpSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")