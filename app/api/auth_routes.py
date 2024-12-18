from fastapi import APIRouter, Depends
from pydantic_models import RegisterSchema, LoginSchema, SuccessResponse, ConflictResponse, InternalServerErrorResponse, LoginResponse, NotFoundResponse, UnauthorizedResponse
from api.common_helper import register_user, login_user
 
auth_router = APIRouter(prefix="/user", tags=["Account"])

@auth_router.post("/register", response_model= SuccessResponse, responses={409: {"model": ConflictResponse}, 500: {"model": InternalServerErrorResponse}})
async def register(user_info: RegisterSchema = Depends()):

    response= await register_user(user_info)
    return SuccessResponse(success=False, message=response['message'])


@auth_router.get("/login", response_model= LoginResponse, responses={401: {"model": UnauthorizedResponse}, 404: {"model": NotFoundResponse}, 500: {"model": InternalServerErrorResponse}})
async def login(user_info: LoginSchema = Depends()):

    response = await login_user(user_info)
    return LoginResponse(access_token = response['access_token'], message= response['message'])
