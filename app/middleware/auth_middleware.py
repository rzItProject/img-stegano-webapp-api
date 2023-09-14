import os
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from fastapi import status


from dotenv import load_dotenv
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class AuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        if request.url.path == "/graphql":  # Check if the request is for the GraphQL endpoint
            token = request.cookies.get("access_token")
            if not token:
                return JSONResponse(status_code=401, content={"detail": "Not authenticated"})
            if token and token.startswith("Bearer "):
                token = token.split("Bearer ")[1]
                try:
                    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                    username: str = payload.get("username")
                    if not username:
                        raise ValueError("Username is missing from token.")
                    request.state.user = username  # Add user information to request state
                    return JSONResponse(status_code=202, content={"detail": "Authenticated"})
                except JWTError:
                    return JSONResponse(status_code=401, content={"detail": "Invalid token"})
        return await call_next(request)