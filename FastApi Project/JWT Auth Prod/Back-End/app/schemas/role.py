from pydantic import BaseModel, ConfigDict
from typing import Optional

class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    id: int
    
    # Enable ORM mode to allow Pydantic to read data even if it is not a dict, but an ORM model
    model_config = ConfigDict(from_attributes=True)
