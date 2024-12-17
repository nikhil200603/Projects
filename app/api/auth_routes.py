from fastapi import APIRouter, Depends
from pydantic_models import RegisterSchema, LoginSchema
from fastapi.responses import JSONResponse
import traceback
from api.common_helper import register_user, login_user

auth_router = APIRouter(prefix="/user", tags=["Account"])

@auth_router.post("/register")
async def register(user_info: RegisterSchema = Depends()):
    try:
        response= await register_user(user_info)
        if response['success']:
            return JSONResponse({"message":response['message']}, status_code=response['status_code'])
        return JSONResponse({"message":response['message']}, status_code=response['status_code'])
    except Exception as e:
        print(traceback.format_exc())
        return JSONResponse({"message":f"Some error occured while registering as {user_info['role']}"},status_code=500)


@auth_router.get("/login")
async def login(user_info: LoginSchema = Depends()):
    try:
        response = await login_user(user_info)
        if response['success']:
            return JSONResponse({"message":response['message'], "token":response['access_token']}, status_code=response['status_code'])
        return JSONResponse({"message":response['message']}, status_code=response['status_code'])
    except Exception as e:
        print(traceback.format_exc())
        return JSONResponse({"message":f"Some error occured"},status_code=500)