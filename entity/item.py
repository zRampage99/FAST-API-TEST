from decimal import Decimal
from sqlmodel import SQLModel, Field
from sqlalchemy import String, Numeric
from typing import Optional

class Item(SQLModel, table=True):
    __tablename__ = "items"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_type=String(50))
    description: str = Field(sa_type=String(200))
    price: Decimal = Field(sa_type=Numeric(precision=10, scale=2))
    is_active: bool = Field(default=True)