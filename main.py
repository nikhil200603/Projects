import uvicorn
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from app.routes import router
from app.database.db import connect_db, disconnect_db
from mangum import Mangum

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


handler= Mangum(app)

@app.get("/")
def home():
    return {"message":"Welcome to Deployed version of Project Assessment"}

