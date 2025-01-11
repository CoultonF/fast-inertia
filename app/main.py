import os
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from inertia import (
    Inertia,
    InertiaConfig,
    InertiaResponse,
    InertiaVersionConflictException,
    inertia_dependency_factory,
    inertia_request_validation_exception_handler,
    inertia_version_conflict_exception_handler,
    lazy,
)
from pydantic import BaseModel, EmailStr
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles

template_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=template_dir)

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="secret_key")
app.add_exception_handler(
    InertiaVersionConflictException,
    inertia_version_conflict_exception_handler,  # type: ignore[arg-type]
)
app.add_exception_handler(
    RequestValidationError,
    inertia_request_validation_exception_handler,  # type: ignore[arg-type]
)
manifest_json = os.path.join(
    os.path.dirname(__file__), "..", "react", "dist", "manifest.json"
)
inertia_config = InertiaConfig(
    templates=templates,
    manifest_json_path=manifest_json,
    environment="development",
    use_flash_messages=True,
    use_flash_errors=True,
    entrypoint_filename="main.ts",
    assets_prefix="/src",
)
InertiaDep = Annotated[Inertia, Depends(inertia_dependency_factory(inertia_config))]
# react_dir = (
#     os.path.join(os.path.dirname(__file__), "..", "react", "dist")
#     if inertia_config.environment != "development"
#     else os.path.join(os.path.dirname(__file__), "..", "react", "src")
# )
# app.mount("/src", StaticFiles(directory=react_dir), name="src")
# app.mount(
#     "/assets", StaticFiles(directory=os.path.join(react_dir, "assets")), name="assets"
# )


# def some_dependency(inertia: InertiaDep) -> None:
#     inertia.share(message="hello from dependency")


@app.get("/", response_model=None)
async def index(inertia: InertiaDep) -> InertiaResponse:
    props = {
        "message": "hello from index",
        "lazy_prop": lazy(lambda: "hello from lazy prop"),
    }
    return await inertia.render("IndexPage", props)


@app.get("/")
async def root():
    return {"message": "Hello World"}


# app/__init__.py
__version__ = "0.1.0"
