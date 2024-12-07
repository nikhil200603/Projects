from fastapi import APIRouter, Depends
from pydantic_models import RegisterSchema, LoginSchema
from fastapi.responses import JSONResponse
import traceback
from api.common_helper import register_user, login_user

auth_router = APIRouter(prefix="/user", tags=["Account"])

@auth_router.post("/register")
async def register(user_info: RegisterSchema = Depends()):
    try:
        user_data = user_info.model_dump()
        success, message = await register_user(user_data)
        if success:
            return JSONResponse({"message":message}, status_code=201)
        return JSONResponse({"message":message}, status_code=400)
    except Exception as e:
        print(traceback.format_exc())
        return JSONResponse({"message":f"Some error occured while registering as {user_info['role']}"},status_code=500)


@auth_router.get("/login")
async def login(user_info: LoginSchema = Depends()):
    try:
        user_data = user_info.model_dump()
        success, token, message = await login_user(user_data)
        if success:
            return JSONResponse({"message":message, "token":token}, status_code=201)
        return JSONResponse({"message":message}, status_code=400)
    except Exception as e:
        print(traceback.format_exc())
        return JSONResponse({"message":f"Some error occured"},status_code=500)