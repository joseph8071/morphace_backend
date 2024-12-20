from pydantic import BaseModel
from typing import Optional, List

class ProductCreate(BaseModel):
    identifier: str
    brand: Optional[str] = None
    name: Optional[str] = None
    type: str
    ingredients: Optional[List[str]] = None

class ProductResponse(BaseModel):
    id: int
    identifier: str
    brand: Optional[str]
    name: Optional[str]
    type: str
    ingredients: List[str]

    class Config:
        orm_mode = True
