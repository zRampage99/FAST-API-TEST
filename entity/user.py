from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import String
from entity.user_role import UserRoleLink

if TYPE_CHECKING:
    from entity.role import Role

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(sa_type=String(50), unique=True)
    hashed_password: str = Field(sa_type=String(255))
    roles: List["Role"] = Relationship(back_populates="users", link_model=UserRoleLink)
