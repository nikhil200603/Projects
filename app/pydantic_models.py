from typing import Optional, Literal, List
from pydantic import BaseModel, Field


class RegisterSchema(BaseModel):
    user_name: str = Field(..., max_length=15,)
    password: str = Field(..., max_length=15)
    role: Literal["admin", "user"]

class LoginSchema(BaseModel):
    user_name: str = Field(..., max_length=15)
    password: str = Field(..., max_length=15)

class ProjectSchema(BaseModel):
    project_title: str = Field(..., max_length=100)
    description: Optional[str] = Field("", max_length=200)
    status: Literal['Active', 'Completed', 'Archived']

class UserSchema(BaseModel):
    user_name: str = Field(..., max_length=15,)
    role: Literal["admin", "user"]

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

class ProjectsFilterSchema(BaseModel):
    page_no: int = Field(1)  # Default value of 1
    title: Optional[str] = None  

class LoginResponse(BaseModel):
    access_token:str
    message:str

class ProjectResponseModel(BaseModel):
    id: str
    project_title: str
    description: str
    status: str
    owner: str

class GetProjectsResponseModel(BaseModel):
    projects: List[ProjectResponseModel]
    message: str

class SuccessResponse(BaseModel):
    success: bool
    message: str

class BadRequestException(BaseModel):
    error_type: str = "BAD_REQUEST_ERROR"
    message: str

class UnauthorizedResponse(BaseModel):
    error_type: str = "UNAUTHORIZED"
    message: str
class NotFoundResponse(BaseModel):
    error_type: str = "RESOURCE_NOT_FOUND"
    message: str

class ForbiddenResponse(BaseModel):
    error_type: str = "ACCESS_FORBIDDEN"
    message: str

class ConflictResponse(BaseModel):
    error_type: str = "DATA_CONFLICT"
    message: str

class InternalServerErrorResponse(BaseModel):
    error_type: str = "INTERNAL_SERVER_ERROR"
    message: str
