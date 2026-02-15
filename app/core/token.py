from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError
from .. import schemas

SECRET_KEY = "8abdfdef0ea2a7fc01888c2a4af6f4269dc2e214ea7fecf52129fac73de89d67"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
