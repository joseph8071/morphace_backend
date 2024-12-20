from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class HabitCreate(BaseModel):
    timestamp: datetime
    sleep_hours: Optional[int] = None
    used_spf: Optional[bool] = None
    skincare_products: Optional[List[str]] = None  # list of product identifiers

class HabitResponse(BaseModel):
    id: int
    timestamp: datetime
    sleep_hours: Optional[int]
    used_spf: Optional[bool]
    skincare_products: List[str]

    class Config:
        orm_mode = True
