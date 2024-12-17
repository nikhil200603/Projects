from fastapi import APIRouter, Depends
from pydantic_models import ProjectSchema
from fastapi.responses import JSONResponse
import traceback
from api.common_helper import save_project_details, get_list_of_projects, update_project_details_by_id, delete_project_by_id
from auth.auth_bearer import JWTBearer
from constants import Role
from auth.authentication import require_roles

project_router = APIRouter(prefix="", tags=["Projects"])

@project_router.post("/projects")
async def create_project(project_info: ProjectSchema = Depends(), user: dict = Depends(require_roles([Role.ADMIN]))):
    try:

        response = await save_project_details(project_info, user)
        return JSONResponse({"message":response['message']}, status_code=response['status_code'])

    except Exception as e:
        print(traceback.format_exc())
        return JSONResponse({"message":"Some error occured while saving project details"},status_code=500)

@project_router.get("/projects")
async def get_project( user: dict = Depends(require_roles([Role.ADMIN, Role.USER]))):
    try:
        response = await get_list_of_projects(user)
        if response['success']:
            return JSONResponse({"projects":response['data'], "message":response['message']}, status_code=response['status_code'])

        return JSONResponse({"message":response['message']}, status_code=response['status_code'])
    except Exception as e:
        print(traceback.format_exc())
        return JSONResponse({"message":"Some error occured while fetching projects"},status_code=500)

@project_router.put("/project/{project_id}")
async def update_project(project_id:str, project_info:ProjectSchema=Depends(), user: dict = Depends(require_roles([Role.ADMIN]))):
    try:
        project_id=project_id
        project_data= project_info.model_dump()
        response= await update_project_details_by_id(project_id, project_data, user)
        return JSONResponse({ "message":response['message']}, status_code = response['status_code'])

    except Exception as e:
        print(traceback.format_exc())
        return JSONResponse({"message":"Some error occured while updating project details."},status_code=500)

@project_router.delete("/project/{project_id}")
async def delete_project(project_id:str, user: dict = Depends(require_roles([Role.ADMIN]))):
    try:
        project_id=project_id
        response= await delete_project_by_id(project_id, user)
        return JSONResponse({"message":response['message']}, status_code=response['status_code'])

    except Exception as e:
        print(traceback.format_exc())
        return JSONResponse({"message":"Some error occured while deleting project."},status_code=500)
