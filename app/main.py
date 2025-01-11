from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager

from app.utils.init_db import create_tables
from app.routers.auth import auth_router
from app.utils.protect_route import get_current_user
from app.schemas.user import UserOutput

@asynccontextmanager
async def lifespan(app : FastAPI):
    # Initialize DB before starting application
    create_tables()
    yield # separated point
    # after yield, we can do something when the application is closing (etc cleaning...)

# dev mode running: fastapi dev main.py
app = FastAPI(lifespan=lifespan)
app.include_router(router=auth_router, tags=["auth"],prefix="/auth")

@app.get("/")
def redirect_to_docs():
    return RedirectResponse(url="/docs")

@app.get('/health')
def health_check():
    return { "status": "health_check" }

@app.get('/protected')
def read_protected(user: UserOutput = Depends(get_current_user)):
    return { "data": user }