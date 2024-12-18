from fastapi import HTTPException

class BadRequestException(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=400, detail=message)
        self.error_type = "Bad Request Error"

class UnauthorizedException(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=401, detail=message)
        self.error_type = "Unauthorized"

class NotFoundException(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=404, detail=message)
        self.error_type = "Resource not Found"

class ForbiddenException(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=403, detail=message)
        self.error_type = "Access Forbidden"

class ConflictException(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=409, detail=message)
        self.error_type = "Data Conflict"

