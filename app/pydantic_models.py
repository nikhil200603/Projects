from typing import Optional, Literal
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
    owner:str = Field(..., max_length=20, description="Project Owner")
