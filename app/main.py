import os
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles

template_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=template_dir)

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="secret_key")
@app.get("/", response_model=None)
async def root():
    props = {
        "message": "hello from index",
        "lazy_prop": lazy(lambda: "hello from lazy prop"),
    }
    return "200"


@app.get("/")
async def root():
    return {"message": "Hello World"}


# app/__init__.py
__version__ = "0.1.0"
