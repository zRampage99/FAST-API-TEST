from pydantic import BaseModel, ConfigDict

class RoleInfo(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)

class UserForClassRole(BaseModel):
    username: str
    
    model_config = ConfigDict(from_attributes=True)
