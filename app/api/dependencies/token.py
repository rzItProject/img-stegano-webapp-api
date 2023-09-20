

from fastapi import Request, HTTPException

def get_token_from_cookie(request: Request):
    token = request.cookies.get("token")
    if not token:
        raise HTTPException(status_code=401, detail="Token is missing from cookies.")
    return token

