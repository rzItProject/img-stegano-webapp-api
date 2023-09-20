import os
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.api.dependencies.auth_dependencies import get_login_service, get_register_service

from app.api.schema.pydantic import LoginSchema, RegisterSchema, ResponseSchema
from app.core.use_cases.auth.login_uc import LoginUser
from app.core.use_cases.auth.register_uc import RegisterUser
from app.infrastructure.database.repositories.user import UsersRepository
from app.infrastructure.database.repositories.auth_repo import JWTRepo


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


@router.post("/login", response_model=ResponseSchema)
async def login_endpoint(req: LoginSchema, login_service: LoginUser = Depends(get_login_service)):
    token = await login_service.login(req)
    response = JSONResponse({"message": "Logged in successfully", "token": token})
    response.set_cookie(
        key="access_token",
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
async def register_endpoint(req: RegisterSchema, register_service: RegisterUser = Depends(get_register_service)):
    print("*********************************")
    print(req)
    print("*********************************")
    await register_service.register(req)
    return ResponseSchema(detail="Successfully save data!")
