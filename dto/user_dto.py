from typing import List
from pydantic import BaseModel, ConfigDict

from dto.item_dto import ItemDtoInfo
from dto.shared_dto import RoleInfo

class UserCredential(BaseModel):
    username: str
    password: str
    
    model_config = ConfigDict(from_attributes=True)

class UserLogged(BaseModel):
    username: str
    access_token: str
    token_type: str = "bearer"
    roles: List[RoleInfo]
    
class UserInfo(BaseModel):
    username: str
    roles: List[RoleInfo]
    items: List[ItemDtoInfo]
    
    model_config = ConfigDict(from_attributes=True)
