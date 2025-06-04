from decimal import Decimal
from sqlmodel import SQLModel, Field
from sqlalchemy import String, Numeric
from typing import Optional
from sqlmodel import SQLModel

class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=String(50))
    description: str = Field(sa_column=String(200))
    price: Decimal = Field(sa_column=Numeric(precision=10, scale=2))
    is_active: bool = Field(default=True)