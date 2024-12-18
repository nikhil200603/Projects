import time
import traceback

import jwt
from passlib.context import CryptContext

from models import User, Project
from config import JwtCred
from pydantic_models import UserSchema, ProjectSchema, RegisterSchema, LoginSchema, ProjectsFilterSchema
from constants import PAGE_SIZE
from exception import ConflictException, ForbiddenException, BadRequestException, NotFoundException, UnauthorizedException

async def hashed_password(password:str): # function to hash password using bcrypt algorithm
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash(password)
    return hashed_password

async def register_user(user_data: RegisterSchema):

    if User.objects(user_name=user_data.user_name.lower()).first():
        raise ConflictException("User with this username already exists")
    
    password = await hashed_password(user_data.password)
    user = User(
        user_name=user_data.user_name.lower(),
        password=password,
        role=user_data.role
    )
    user.save()  # Save the user in MongoDB
    return {"success": True, "message": "User Registered Successfully", "status_code": 201}

async def verify_password (given_password:str, hashed_password:str):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(given_password, hashed_password)

async def get_access_token(user_info:UserSchema, role:str, expiry:int, token_type:str):
    payload = {
        "user_name": user_info.user_name,
        "role": role,
        "token_type": token_type,
        "expires": time.time() + expiry
    }
    token = jwt.encode(payload, JwtCred.JWT_SECRET, algorithm=JwtCred.JWT_ALGORITHM)
    return token

async def login_user(user_data: LoginSchema):

    if not User.objects(user_name= user_data.user_name).first():
        raise NotFoundException("User not found.")

    if User.objects(user_name=user_data.user_name).first():
        object = User.objects(user_name=user_data.user_name).first()
        password_verified = await verify_password(user_data.password, object.password)

        if password_verified:
            access_token = await get_access_token(user_data, object.role, JwtCred.JWT_VALIDITY, JwtCred.ACCESS_TOKEN )
            return {"success": True, "access_token": access_token, "message": "Logged In successfully", "status_code": 200}

    raise UnauthorizedException("Incorrect password")

async def save_project_details(project_data:ProjectSchema, user:UserSchema):

    if Project.objects(project_title=project_data.project_title).first():
        raise ConflictException("Project with same Title Exist")
    
    project = Project(
        project_title=project_data.project_title,
        description=project_data.description,
        status=project_data.status,
        owner=user.user_name
    )
    project.save()
    return {"success": True, "message": "Project Details Saved Successfully"}

async def get_list_of_projects(project_filter:ProjectsFilterSchema):

    skip_count = (project_filter.page_no-1)*PAGE_SIZE
    if project_filter.title:
        projects=Project.objects(project_title__iregex=project_filter.title).skip(skip_count).limit(PAGE_SIZE)
    else:
        projects=Project.objects().skip(skip_count).limit(PAGE_SIZE)

    if not projects:
        raise NotFoundException("Projects Not Found")

    project_list=[]
    for project in projects:
        project_dict=dict(project.to_mongo())
        project_dict['id']=str(project_dict['_id'])
        project_list.append(project_dict)

    return {"success": True, "data": project_list, "message": "Projects fetched successfully"}

async def update_project_details_by_id(project_id:str, project_data:ProjectSchema, user:UserSchema):

    if len(project_id) != 24:
        raise BadRequestException("Invalid Project ID")

    project_obj = Project.objects.filter(id=project_id)
    if not project_obj:
        raise NotFoundException("Invalid Project ID")

    if Project.objects.filter(id=project_id).first().owner != user.user_name:
        raise ForbiddenException("You are not permitted to perform this action")

    if Project.objects.filter(id__ne=project_id, project_title=project_data.project_title).first():
        raise ConflictException("Project with the given Project Title already exists")

    project_data = project_data.model_dump()
    project_obj.update(**project_data)
    return {"message": "Project details updated successfully"}

async def delete_project_by_id(project_id:str, user:UserSchema):

    if len(project_id)!=24:
        raise BadRequestException("Invalid Project ID")

    project_obj = Project.objects.filter(id=project_id).first()
    if not project_obj:
        raise NotFoundException("Project not found")
    
    if project_obj.owner != user.user_name:
        raise ForbiddenException("You are not permitted to perform this action")

    project_obj.delete()
    return {"message": "Project details deleted successfully", "status_code": 200}
