from fastapi import APIRouter, Depends, HTTPException
from pydantic_models import ProjectSchema, ProjectsFilterSchema, SuccessResponse, ConflictResponse, ForbiddenResponse, BadRequestException, InternalServerErrorResponse, GetProjectsResponseModel, NotFoundResponse, UserSchema
from fastapi.responses import JSONResponse
import traceback
from api.common_helper import save_project_details, get_list_of_projects, update_project_details_by_id, delete_project_by_id
from auth.auth_bearer import JWTBearer
from constants import Role
from auth.authentication import require_roles

project_router = APIRouter(prefix="", tags=["Projects"])

@project_router.post("/projects",  response_model=SuccessResponse, responses={409: {"model": ConflictResponse}, 500: {"model": InternalServerErrorResponse}})
async def create_project(project_info: ProjectSchema = Depends(), user: UserSchema = Depends(require_roles([Role.ADMIN]))):

    response = await save_project_details(project_info, user)
    return SuccessResponse(success=response['success'], message=response['message'])


@project_router.get("/projects", response_model= GetProjectsResponseModel, responses={404: {"model": NotFoundResponse}, 409: {"model": ConflictResponse}, 500: {"model": InternalServerErrorResponse}})
async def get_project( project_filters:ProjectsFilterSchema = Depends(), user: UserSchema = Depends(require_roles([Role.ADMIN, Role.USER]))):

    response = await get_list_of_projects(project_filters)
    return  GetProjectsResponseModel(projects=response['data'], message = response["message"])


@project_router.put("/project/{project_id}", response_model=SuccessResponse, responses={400: {"model": BadRequestException}, 403: {"model": ForbiddenResponse},  404: {"model": NotFoundResponse}, 409: {"model": ConflictResponse}, 500: {"model": InternalServerErrorResponse}})
async def update_project(project_id:str, project_info:ProjectSchema=Depends(), user: UserSchema = Depends(require_roles([Role.ADMIN]))):

    project_id=project_id
    response= await update_project_details_by_id(project_id, project_info, user)
    return SuccessResponse(success=True, message= response['message'])


@project_router.delete("/project/{project_id}", response_model=SuccessResponse, responses={400: {"model": BadRequestException}, 403: {"model": ForbiddenResponse}, 404: {"model": NotFoundResponse}, 500: {"model": InternalServerErrorResponse}})
async def delete_project(project_id:str, user: UserSchema = Depends(require_roles([Role.ADMIN]))):

    response= await delete_project_by_id(project_id, user)
    return SuccessResponse(success=True, message= response['message'])

