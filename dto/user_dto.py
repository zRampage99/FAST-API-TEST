from typing import List
from pydantic import BaseModel, ConfigDict

from dto.role_dto import RoleDto

class UserCredential(BaseModel):
    username: str
    password: str
    
    model_config = ConfigDict(from_attributes=True)

class UserLogged(BaseModel):
    username: str
    access_token: str
    token_type: str = "bearer"
    roles: List[RoleDto]
    
class UserInfo(BaseModel):
    username: str
    roles: List[RoleDto]
    
    model_config = ConfigDict(from_attributes=True)
