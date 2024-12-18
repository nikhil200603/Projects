import uvicorn
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from routes import router
from database.db import connect_db, disconnect_db
from exception import ConflictException, NotFoundException, ForbiddenException, BadRequestException

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        connect_db()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    yield
    disconnect_db()


app= FastAPI(lifespan=lifespan)
app.include_router(router)

@app.exception_handler(BadRequestException)
async def unauthorized_exception_handler(request: Request, exc: BadRequestException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error_type": exc.error_type, "message": exc.detail},
    )

@app.exception_handler(NotFoundException)
async def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error_type": exc.error_type, "message": exc.detail},
    )

@app.exception_handler(ForbiddenException)
async def forbidden_exception_handler(request: Request, exc: ForbiddenException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error_type": exc.error_type, "message": exc.detail},
    )

@app.exception_handler(ConflictException)
async def conflict_exception_handler(request: Request, exc: ConflictException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error_type": exc.error_type, "message": exc.detail},
    )

@app.exception_handler(Exception)
async def internal_server_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error_type": "Internal Server Error",
            "message": "An unexpected error occurred. Please try again later."
        },
    )

@app.get("/home")
def home():
    return {"message":"HELLO WORLD"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)