from pydantic import BaseModel, ConfigDict

class UserDto(BaseModel):
    username: str
    password: str
    model_config = ConfigDict(from_attributes=True)

class UserLogged(BaseModel):
    username: str
    access_token: str
    token_type: str = "bearer"
