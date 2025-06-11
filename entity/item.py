from decimal import Decimal
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import String, Numeric
from typing import Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from entity.user import User
class Item(SQLModel, table=True):
    __tablename__ = "items"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_type=String(50))
    description: str = Field(sa_type=String(200))
    price: Decimal = Field(sa_type=Numeric(precision=10, scale=2))
    is_active: bool = Field(default=True)

    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    #E' facoltativo nel database, 
    # ma obbligatorio nel DTO e viene associato tramite l'ID dentro il payload di JWT
    user: Optional["User"] = Relationship(back_populates="items")