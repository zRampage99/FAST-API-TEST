from pydantic import BaseModel, ConfigDict, Field
from decimal import Decimal
from typing import Annotated
from typing import Optional

# BaseModel è la classe base di tutti i modelli dati (DTO) in Pydantic
class ItemCreate(BaseModel):
    name: Annotated[str, Field(min_length=3, max_length=50)]
    description: Annotated[str, Field(max_length=200)]
    price: Annotated[Decimal, Field(max_digits=10, decimal_places=2)]

    #@field_validator("price")
    #def round_price(cls, v):
    #    return round(v, 2) # Può accettare valori con 3 o più decimali ed arrotonda in automatico

class ItemRead(BaseModel):
    id: int
    name: str
    description: str
    price: float
    is_active: bool
    
    # Serve per abilitare il supporto alla mappatura da oggetti ORM
    model_config = ConfigDict(from_attributes=True)

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    is_active: Optional[bool] = None
