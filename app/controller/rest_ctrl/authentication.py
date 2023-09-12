import json
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.schema.pydantic import (
    ResponseSchema,
    RegisterSchema,
    LoginSchema,
)
from app.service.authentication import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register", response_model=ResponseSchema, response_model_exclude_none=True
)
async def register(request_body: RegisterSchema):
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
        max_age=600,
        samesite="lax",
        secure=True,
    )
    return response



