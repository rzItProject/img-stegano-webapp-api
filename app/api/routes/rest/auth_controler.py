import os
from typing import Any
from fastapi import APIRouter, Depends, File, Request, UploadFile
from fastapi.responses import JSONResponse
from app.api.dependencies.repo_dependencies import get_login_uc, get_register_uc
from app.api.dependencies.user import get_current_user

from app.api.schema.pydantic import LoginSchema, RegisterSchema, ResponseSchema
from app.core.use_cases.auth.login_uc import LoginUseCase
from app.core.use_cases.auth.register_uc import RegisterUseCase
from app.infrastructure.database.orm_models.users import Users
from app.infrastructure.database.repositories.user import UsersRepository
from app.api.auth_repo import JWTRepo


from dotenv import load_dotenv

load_dotenv()

COOKIE_EXPIRE_SECONDE = os.getenv("COOKIE_EXPIRE_SECONDE")
try:
    COOKIE_EXPIRE_SECONDE = int(COOKIE_EXPIRE_SECONDE)
except (TypeError, ValueError):
    raise ValueError(
        "La variable d'environnement COOKIE_EXPIRE_SECONDE doit être un nombre entier valide."
    )

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.get("/check_status")
async def check_auth(user: Users = Depends(get_current_user)):
    if user is None:
        return {"isAuth": False}
    return {"isAuth": True, "user": user}


@router.post("/login", response_model=ResponseSchema)
async def user_login(
    req: LoginSchema, login_use_case: LoginUseCase = Depends(get_login_uc)
):
    token = await login_use_case.login(req)
    response = JSONResponse({"message": "Logged in successfully", "token": token})
    response.set_cookie(
        key="token",
        value=token,
        httponly=True,
        max_age=COOKIE_EXPIRE_SECONDE,
        samesite="none",
        secure=True,  # mettre à TRUE pour s'assurer que le cookie ne soit envoyé que au requete HTTPS
    )
    return response


@router.post(
    "/register", response_model=ResponseSchema, response_model_exclude_none=True
)
async def user_register(
    req: RegisterSchema, register_service: RegisterUseCase = Depends(get_register_uc)
):
    user = await register_service.register(req)
    print(user)
    return ResponseSchema(detail="Successfully save data!")
