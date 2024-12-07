import uvicorn
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from routes import router
from database.db import connect_db, disconnect_db

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

@app.get("/home")
def home():
    return {"message":"HELLO WORLD"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)