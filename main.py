# main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from handler.Exception import register_exception_handlers
from db import engine
from controller.itemController import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield
    # Eventuali operazioni di cleanup possono essere aggiunte qui
app = FastAPI(lifespan=lifespan)
register_exception_handlers(app)
app.include_router(router)
