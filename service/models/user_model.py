from enum import Enum
from typing import Optional
from pydantic import BaseModel, conlist

class MaritalStatus(str, Enum):
    single = "single"
    married = "married"
    def __getitem__(self, item):
        return getattr(self, item)

class OwnershipStatus(str, Enum):
    owned = "owned"
    mortgaged = "mortgaged"
    def __getitem__(self, item):
        return getattr(self, item)

class House(BaseModel):
    ownership_status: OwnershipStatus
    def __getitem__(self, item):
        return getattr(self, item)

class Vehicle(BaseModel):
    year: int
    def __getitem__(self, item):
        return getattr(self, item)

class UserModel(BaseModel):

    age: int
    dependents: int
    house: Optional[House] = None
    income: int
    marital_status: MaritalStatus
    risk_questions: conlist(int, min_items=3, max_items=3)
    vehicle: Optional[Vehicle] = None
    def __getitem__(self, item):
        return getattr(self, item)

    class Config:
        schema_extra = {
            "example": {
                "age": 35,
                "dependents": 2,
                "house": {"ownership_status": "owned"},
                "income": 0,
                "marital_status": "married",
                "risk_questions": [0, 1, 0],
                "vehicle": {"year": 2018}
            }
        }

