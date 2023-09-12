import os
from datetime import datetime, timedelta
from typing import Optional
from dotenv import load_dotenv
from jose import JWTError, jwt

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 15


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
            return decode_token if decode_token["exp"] >= datetime.time() else None
        except:
            return {}
    
    def verify_jwt(self, token: str):
        try:
            payload = self.decode_token(token)
            user_id = payload.get("user_id")
            
            if not user_id:
                return None

            return user_id

        except JWTError:
            return None
    
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
