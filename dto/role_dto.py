from typing import List
from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated
from typing import Optional

from dto.shared_dto import UserForClassRole



class RoleDto(BaseModel):
    id: int
    name: str
    users: List[UserForClassRole]
    
class RoleDtoCreate(BaseModel):
    name: str = Annotated[str, Field(max_length=200)]
    users: List[UserForClassRole]

    model_config = ConfigDict(from_attributes=True)