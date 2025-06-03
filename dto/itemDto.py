from pydantic import BaseModel
from typing import Optional

class ItemCreate(BaseModel):
    name: str
    description: str
    price: float

class ItemRead(BaseModel):
    id: int
    name: str
    description: str
    price: float
    is_active: bool

    class Config:
        orm_mode = True

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    is_active: Optional[bool] = None
