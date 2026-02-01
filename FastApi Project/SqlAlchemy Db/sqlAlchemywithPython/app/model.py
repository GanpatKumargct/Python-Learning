from pydantic import BaseModel


# Schema model - DTO 
class Product(BaseModel):

    id :int
    name : str
    description : str
    price : float
    quantity  : int
