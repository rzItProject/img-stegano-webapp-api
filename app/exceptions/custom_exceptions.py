from fastapi import HTTPException


class InvalidPasswordException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=422, detail=detail)


class InvalidUsernameException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=422, detail=detail)


class InvalidBirthdateException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=422, detail=detail)


class InvalidGenderException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=422, detail=detail)


class InvalidEmailException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=422, detail=detail)


class UsernameNotFoundException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=401, detail=detail)


class UsernameAlreadyExistException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=401, detail=detail)


class EmailAlreadyExistsException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=401, detail=detail)


class InvalidDataException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=401, detail=detail)


class TokenMissingException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=401,
            detail={"isAuth": False, "message": "Token is missing from request."},
        )


class InvalidTokenException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=401,
            detail={
                "isAuth": False,
                "message": "Invalid token or token could not be decoded.",
            },
        )


class TokenExpiredException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=401, detail={"isAuth": False, "message": "Token has expired."}
        )


class UserNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail={
                "isAuth": False,
                "message": "User associated with token not found.",
            },
        )


class InsufficientPermissionsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=403, detail="User does not have sufficient permissions."
        )
