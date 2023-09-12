""" import os
from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from fastapi.responses import JSONResponse
from jose import JWTError, jwt
from dotenv import load_dotenv

from app.utils.security import create_access_token
from app.schema.pydantic import CreateUserInput, LoginUserInput, Token, TokenData
from app.service.authentication import UserService

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

router = APIRouter(prefix='/auth', tags=['auth'])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

@router.post("/register")
async def register(user_data: CreateUserInput):
    user = await UserService.register_user(user_data)
    if not user:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="A user with the provided email or username already exists.")
    return {"message": "Successful registration",}
    
@router.post('/login', response_model=Token)
async def login_for_access(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await UserService.authenticate_user(LoginUserInput(username=form_data.username, password=form_data.password))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(data={"user_id": user.id, "username": user.username}, expires_delta=timedelta(minutes=10))
    response = JSONResponse({"message": "Logged in successfully"})
    response.set_cookie(key="access_token", value=token, httponly=True, max_age=600, samesite="lax", secure=True)  # Set cookie for 1 hour
    return response

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
    user = await UserService.fetch_user_by_username(token_data.username)
    if user is None:
        raise user_token_exception
    return user
    
 """