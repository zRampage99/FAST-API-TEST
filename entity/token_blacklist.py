from sqlmodel import SQLModel, Field
from typing import Optional

class TokenBlacklist(SQLModel, table=True):
    __tablename__ = "tokens_blacklist"
    id: Optional[int] = Field(default=None, primary_key=True)
    token: str
