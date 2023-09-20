import json
import os
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from app.infrastructure.database.repositories.auth_repo import JWTRepo
load_dotenv()

from app.api.schema.pydantic import (
    ResponseSchema,
    RegisterSchema,
    LoginSchema,
)
from app.core.authentication import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])

COOKIE_EXPIRE_SECONDE = os.getenv("COOKIE_EXPIRE_SECONDE")
try:
    COOKIE_EXPIRE_SECONDE = int(COOKIE_EXPIRE_SECONDE)
except (TypeError, ValueError):
    raise ValueError("La variable d'environnement COOKIE_EXPIRE_SECONDE doit être un nombre entier valide.")

@router.get("/check-auth")
async def check_auth(request: Request):
    # Récupérer le cookie directement à partir de l'objet request
    authToken = request.cookies.get("access_token", None)
    print("******************************************")
    print(authToken)
    if authToken is None:
        raise HTTPException(status_code=401, detail="Token a expiré ou invalide")
    
    if JWTRepo(token=authToken).decode_token() is None:
        return {"authenticated": False}
    return {"authenticated": True}


@router.post(
    "/register", response_model=ResponseSchema, response_model_exclude_none=True
)
async def register(request_body: RegisterSchema):
    print(request_body)
    await AuthService.register_service(request_body)
    return ResponseSchema(detail="Successfully save data!")


@router.post("/login", response_model=ResponseSchema)
async def login(requset_body: LoginSchema):
    token = await AuthService.logins_service(requset_body)
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



