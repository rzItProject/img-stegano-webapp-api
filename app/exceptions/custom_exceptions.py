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
