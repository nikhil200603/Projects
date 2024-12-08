from fastapi import APIRouter

from app.api.projects_routes import project_router
from app.api.auth_routes import auth_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(project_router)
