from enum import Enum
from pydantic import BaseModel

class Results(str, Enum):
    inelegible = "ineligible"
    economic = "economic"
    regular = "regular"
    responsible = "responsible"
    def __getitem__(self, item):
        return getattr(self, item)


class RiskModel(BaseModel):
    auto: Results
    disability: Results
    home: Results
    life: Results
    def __getitem__(self, item):
        return getattr(self, item)

    class Config:
        schema_extra = {
            "example": {
            "auto": "regular",
            "disability": "ineligible",
            "home": "economic",
            "life": "regular"
            }
        }