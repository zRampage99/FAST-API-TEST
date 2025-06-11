from pydantic import BaseModel, ConfigDict, Field
from decimal import Decimal
from typing import Annotated
from typing import Optional

# BaseModel è la classe base di tutti i modelli dati (DTO) in Pydantic
class ItemDto(BaseModel):
    id: int
    name: str
    description: str
    price: float
    is_active: bool
    user_id: int
    
    # Serve per abilitare il supporto alla mappatura da oggetti ORM
    model_config = ConfigDict(from_attributes=True)

class ItemDtoCreate(BaseModel):
    name: Annotated[str, Field(min_length=3, max_length=50)]
    description: Annotated[str, Field(max_length=200)]
    price: Annotated[Decimal, Field(max_digits=10, decimal_places=2)]
    #user_id: Annotated[int, Field(ge=1)] # Assicurati che user_id sia un intero positivo

    # Abilitare questo metodo per accettare valori con 3 o più decimali ed arrotonda in automatico
    #@field_validator("price")
    #def round_price(cls, v):
    #    return round(v, 2)

class ItemDtoUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3, max_length=50)
    description: Optional[str] = Field(default=None, max_length=200)
    price: Optional[Decimal] = Field(default=None, max_digits=10, decimal_places=2)
    is_active: Optional[bool] = None
    user_id: Optional[int] = None

class ItemDtoInfo(BaseModel):
    id: int
    name: str
    description: str
    price: float
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
