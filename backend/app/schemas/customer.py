from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional

class CustomerBase(BaseModel):
    age: int
    income: float
    segment_label: Optional[str] = None
    campaign_id: Optional[UUID] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerRead(CustomerBase):
    id: UUID
    
    model_config = ConfigDict(from_attributes=True)
