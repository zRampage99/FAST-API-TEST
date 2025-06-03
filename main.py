# main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from db import engine
from controller.itemController import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield
    # Eventuali operazioni di cleanup possono essere aggiunte qui

app = FastAPI(lifespan=lifespan)
app.include_router(router)
