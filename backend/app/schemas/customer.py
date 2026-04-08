from pydantic import BaseModel
from typing import Optional

# customer
class CustomerCreate(BaseModel):
    age: int
    income: float

class CustomerResponse(BaseModel):
    id: str
    age: int
    income: float
    segment_label: Optional[str] = None

    class Config:
        from_attributes = True