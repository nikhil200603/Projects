import time
import traceback

import jwt
from passlib.context import CryptContext
from bson import ObjectId

from app.models import User, Project
from app.config import JwtCred

async def hashed_password(password): # function to hash password using bcrypt algorithm
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash(password)
    return hashed_password

async def register_user(user_data):
    try:
        if User.objects(user_name=user_data['user_name']).first():
            return False, "User with this username already exist"
        
        password = await hashed_password(user_data.get('password'))
        user = User(
            user_name=user_data.get('user_name'),
            password=password,
            role=user_data.get('role')
        )
        user.save()  # Save the user in MongoDB
        return True, "User Registered Successfully"

    except Exception as e:
        print(traceback.format_exc())
        return False, "Some error occured"

async def verify_password (given_password, hashed_password):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(given_password, hashed_password)

async def get_access_token(user_info, expiry, token_type):
    payload = {
        "user_name": user_info['user_name'],
        "role": user_info['role'],
        "token_type": token_type,
        "expires": time.time() + expiry
    }
    token = jwt.encode(payload, JwtCred.JWT_SECRET, algorithm=JwtCred.JWT_ALGORITHM)
    return token

async def login_user(user_data):
    try:
        if not User.objects(user_name= user_data['user_name']).first():
            return False, None, "username is incorrect"

        if User.objects(user_name=user_data['user_name']).first():
            object = User.objects(user_name=user_data['user_name']).first()
            password_verified = await verify_password(user_data['password'], object.password)

            if password_verified:
                user_data['role'] = object.role
                access_token = await get_access_token(user_data, JwtCred.JWT_VALIDITY, JwtCred.ACCESS_TOKEN )
                return True, access_token, "Logged In successfully"

        return False, None, "Incorrect Password"

    except Exception as e:
        print(traceback.format_exc())
        return False, None, "Some error occured"

async def save_project_details(project_data):
    try:
        if Project.objects(project_title=project_data['project_title']).first():
            return False, "Project with given title already exist"
        
        project = Project(
            project_title=project_data['project_title'],
            description=project_data['description'],
            status=project_data['status'],
            owner=project_data['owner']
        )
        project.save()
        return True, "Project Details Saved Successfully"

    except Exception as e:
        print(traceback.format_exc())
        return False, "Some error occured"

async def get_list_of_projects():
    try:
        projects=Project.objects()
        if not projects:
            return True, [], "No Projects Found"

        project_list=[]
        for project in projects:
            project_dict=project.to_mongo()
            project_dict['_id']=str(project_dict['_id'])
            project_list.append(project_dict)

        return True, project_list, "Projects fetched successfully"
    except Exception as e:
        print(traceback.format_exc())
        return False, None, "Some error occured"

async def update_project_details_by_id(project_id, project_data):
    try:
        if len(project_id)!=24:
            return False, "Invalid Project ID"

        project_obj = Project.objects.filter(id=project_id)

        if not project_obj:
            return False, "Invalid Project ID"

        if Project.objects.filter(id__ne=project_id, project_title = project_data['project_title']).first():
            return False, "Project with given Project Title already exists"

        project_obj.update(**project_data)
        return True, "Project details updated successfully"

    except Exception as e:
        print(traceback.format_exc())
        return False, "Some error occured"
    
async def delete_project_by_id(project_id):
    try:
        if len(project_id)!=24:
            return False, "Invalid Project ID"

        project_obj = Project.objects.filter(id=project_id)
        if not project_obj:
            return False, "Invalid Project ID"

        project_obj.delete()
        return True, "Project details deleted successfully"
    except Exception as e:
        print(traceback.format_exc())
        return False, "Some error occured"
