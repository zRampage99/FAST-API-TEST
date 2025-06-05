from sqlmodel import SQLModel, Field
from sqlalchemy import String
from typing import Optional

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(sa_type=String(50), unique=True)
    hashed_password: str = Field(sa_type=String(255))
