from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import String
from entity.user_role import UserRoleLink

if TYPE_CHECKING:
    from entity.user import User

class Role(SQLModel, table=True):
    __tablename__ = "roles"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_type=String(50), unique=True)
    users: List["User"] = Relationship(back_populates="roles", link_model=UserRoleLink)

