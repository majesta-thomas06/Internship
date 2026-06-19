from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from .database import SessionLocal
from .models import Employee
from . import models
from .database import engine, Base
from .routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Audit Tracking Framework"
)

app.include_router(router)

templates = Jinja2Templates(
    directory="templates"
)


@app.get("/")
def home():
    return {
        "message": "Audit Tracking Framework"
    }



