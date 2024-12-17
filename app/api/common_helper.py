import time
import traceback

import jwt
from passlib.context import CryptContext
from bson import ObjectId

from models import User, Project
from config import JwtCred
from pydantic_models import UserSchema, ProjectSchema, RegisterSchema, LoginSchema

async def hashed_password(password:str): # function to hash password using bcrypt algorithm
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash(password)
    return hashed_password

async def register_user(user_data: RegisterSchema):
    try:
        if User.objects(user_name=user_data.user_name.lower()).first():
            return {"success": False, "message": "User with this username already exists", "status_code": 409}
        
        password = await hashed_password(user_data.password)
        user = User(
            user_name=user_data.user_name.lower(),
            password=password,
            role=user_data.role
        )
        user.save()  # Save the user in MongoDB
        return {"success": True, "message": "User Registered Successfully", "status_code": 201}

    except Exception as e:
        print(traceback.format_exc())
        return {"success": False, "message": "Some error occurred", "status_code": 500}

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
    try:
        if not User.objects(user_name= user_data.user_name).first():
            return {"success": False, "access_token": None, "message": "Username is incorrect", "status_code": 404}

        if User.objects(user_name=user_data.user_name).first():
            object = User.objects(user_name=user_data.user_name).first()
            password_verified = await verify_password(user_data.password, object.password)

            if password_verified:
                access_token = await get_access_token(user_data, object.role, JwtCred.JWT_VALIDITY, JwtCred.ACCESS_TOKEN )
                return {"success": True, "access_token": access_token, "message": "Logged In successfully", "status_code": 200}

        return {"success": False, "access_token": None, "message": "Incorrect password", "status_code": 401}

    except Exception as e:
        print(traceback.format_exc())
        return {"success": False, "access_token": None, "message": "Some error occurred", "status_code": 500}

async def save_project_details(project_data:ProjectSchema, user:UserSchema):
    try:
        if Project.objects(project_title=project_data.project_title).first():
            return {"success": False, "message": "Project with given title already exists", "status_code": 409}
        
        project = Project(
            project_title=project_data.project_title,
            description=project_data.description,
            status=project_data.status,
            owner=user.user_name
        )
        project.save()
        return {"success": True, "message": "Project Details Saved Successfully", "status_code": 201}

    except Exception as e:
        print(traceback.format_exc())
        return {"success": False, "message": "Some error occurred", "status_code": 500}

async def get_list_of_projects(user:UserSchema):
    try:
        projects=Project.objects()
        if not projects:
            return {"success": True, "data": [], "message": "No Projects Found", "status_code": 200}

        project_list=[]
        for project in projects:
            project_dict=project.to_mongo()
            project_dict['_id']=str(project_dict['_id'])
            project_list.append(project_dict)

        return {"success": True, "data": project_list, "message": "Projects fetched successfully", "status_code": 200}
    except Exception as e:
        print(traceback.format_exc())
        return {"success": False, "data": None, "message": "Some error occurred", "status_code": 500}

async def update_project_details_by_id(project_id:str, project_data:dict, user:UserSchema):
    try:
        if len(project_id) != 24:
            return {"message": "Invalid Project ID", "status_code": 400}

        project_obj = Project.objects.filter(id=project_id)

        if not project_obj:
            return {"message": "Invalid Project ID", "status_code": 400}

        if Project.objects.filter(id=project_id).first().owner != user.user_name:
            return {"message": "You are not permitted to perform this action", "status_code": 403}

        if Project.objects.filter(id__ne=project_id, project_title=project_data['project_title']).first():
            return {"message": "Project with given Project Title already exists", "status_code": 409}

        project_obj.update(**project_data)
        return {"message": "Project details updated successfully", "status_code": 200}

    except Exception as e:
        print(traceback.format_exc())
        return {"message": "Some error occurred", "status_code": 500}

async def delete_project_by_id(project_id:str, user:UserSchema):
    try:
        if len(project_id)!=24:
            return {"message": "Invalid Project ID", "status_code": 400}

        project_obj = Project.objects.filter(id=project_id).first()
        if not project_obj:
            return {"message": "Invalid Project ID", "status_code": 400}
        
        if project_obj.owner != user.user_name:
            return {"message": "You are not permitted to perform this action", "status_code": 403}

        project_obj.delete()
        return {"message": "Project details deleted successfully", "status_code": 200}
    except Exception as e:
        print(traceback.format_exc())
        return {"message": "Some error occurred", "status_code": 500}
