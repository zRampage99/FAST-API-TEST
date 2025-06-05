from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from repository.db import engine
from controller.item_controller import item_router
from controller.auth_controller import auth_router
from controller.health_check_controller import health_check_router
from handler.exception import register_exception_handlers
from entity.token_blacklist import TokenBlacklist

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield
    # Eventuali operazioni di cleanup possono essere aggiunte qui
app = FastAPI(lifespan=lifespan)
register_exception_handlers(app)
app.include_router(item_router)
app.include_router(auth_router)
app.include_router(health_check_router)