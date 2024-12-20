# app/schemas/sensor.py
from pydantic import BaseModel, conlist, confloat
from typing import List, Optional
from datetime import datetime

class ImpedanceData(BaseModel):
    freq: conlist(confloat(ge=0), min_items=1)
    reZ: conlist(confloat(ge=0), min_items=1)
    imZ: conlist(confloat(ge=0), min_items=1)
    magZ: conlist(confloat(ge=0), min_items=1)
    phase: conlist(confloat(ge=0), min_items=1)

    # Validate that all arrays have the same length
    def validate_arrays(self):
        lengths = [
            len(self.freq), len(self.reZ), len(self.imZ),
            len(self.magZ), len(self.phase)
        ]
        if len(set(lengths)) != 1:
            raise ValueError("All impedance arrays must have the same length.")

    def __init__(self, **data):
        super().__init__(**data)
        self.validate_arrays()

class SensorDataCreate(BaseModel):
    timestamp: datetime
    sensor_id: Optional[int] = None
    humidity: conlist(confloat(), min_items=10, max_items=10)
    temperature: conlist(confloat(), min_items=10, max_items=10)
    impedance: ImpedanceData

class SensorDataResponse(BaseModel):
    id: int
    timestamp: datetime
    sensor_id: Optional[int]
    user_id: str
    humidity: List[float]
    temperature: List[float]
    impedance: dict  # or more structured if needed

    class Config:
        orm_mode = True
