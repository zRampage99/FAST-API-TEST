from pydantic import BaseModel, ConfigDict

class RoleDto(BaseModel):
    name: str
    
    model_config = ConfigDict(from_attributes=True)