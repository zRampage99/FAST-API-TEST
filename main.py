from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from repository.db import engine, init_roles
from controller.item_controller import item_router
from controller.user_controller import auth_router
from controller.role_controller import role_router
from controller.health_check_controller import health_check_router
from handler.exception import register_exception_handlers
from entity.user import User
from entity.role import Role

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    init_roles()
    yield
    # Eventuali operazioni di cleanup possono essere aggiunte qui
app = FastAPI(lifespan=lifespan)
register_exception_handlers(app)
app.include_router(item_router)
app.include_router(auth_router)
app.include_router(role_router)
app.include_router(health_check_router)