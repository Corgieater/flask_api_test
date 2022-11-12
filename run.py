from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.staticfiles import StaticFiles
from app import class_file
from app.models import order_models
from app.models import auth
import uvicorn
from app.routers import router
app = FastAPI()
app.include_router(router)

app.mount("/static", StaticFiles(directory="app/templates/static"), name="static")

