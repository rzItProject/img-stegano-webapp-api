import os
from datetime import datetime, timedelta
from typing import Optional
from dotenv import load_dotenv
from jose import JWTError, jwt

from fastapi import Depends, Request, HTTPException, status
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
    OAuth2PasswordBearer,
)
from app.infrastructure.database.repository.user import UsersRepository


from app.api.schema.pydantic import TokenData

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
try:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(ACCESS_TOKEN_EXPIRE_MINUTES)
except (TypeError, ValueError):
    raise ValueError("La variable d'environnement ACCESS_TOKEN_EXPIRE_MINUTES doit être un nombre entier valide.")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


class JWTRepo:
    def __init__(self, data: dict = {}, token: str = None):
        self.data = data
        self.token = token

    def create_access_token(self, expires_delta: Optional[timedelta] = None):
        to_encode = self.data.copy()
        # Ajout d'un horodatage
        to_encode["iat"] = datetime.utcnow()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    
    def decode_token(self):
        try:
            decode_token = jwt.decode(self.token, SECRET_KEY, algorithms=[ALGORITHM])
            print(decode_token["exp"])
            if decode_token["exp"] >= datetime.utcnow().timestamp():
                return decode_token
            else:
                raise HTTPException(status_code=401, detail="Token a expiré")    
        except JWTError:
            raise HTTPException(status_code=401, detail="Token invalide")

    @staticmethod
    def verify_jwt(jwt_token: str):
        return (
            True
            if jwt.decode(jwt_token, SECRET_KEY, algorithms=[ALGORITHM]) is not None
            else False
        )

    """ def verify_jwt(self, token: str):
        try:
            payload = self.decode_token(token)
            user_id = payload.get("user_id")
            
            if not user_id:
                return None

            return user_id

        except JWTError:
            return None """

    @staticmethod
    def extract_token(token: str):
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403,
                    detail={
                        "status": "Forbidden",
                        "message": "Invalid authentication schema.",
                    },
                )
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403,
                    detail={
                        "status": "Forbidden",
                        "message": "Invalid token or expired token.",
                    },
                )
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=403,
                detail={
                    "status": "Forbidden",
                    "message": "Invalid authorization code.",
                },
            )

    @staticmethod
    def verify_jwt(jwt_token: str):
        return (
            True
            if jwt.decode(jwt_token, SECRET_KEY, algorithms=[ALGORITHM]) is not None
            else False
        )


# not used because we are using a middleware and cookies
async def get_current_user(token: str = Depends(oauth2_scheme)):
    user_token_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate user",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        user_id: str = payload.get("user_id")
        if username is None or user_id is None:
            raise user_token_exception
        token_data = TokenData(username=username, user_id=user_id)
    except JWTError:
        raise user_token_exception
    user = await UsersRepository.find_by_username(token_data.username)
    if user is None:
        raise user_token_exception
    return user
