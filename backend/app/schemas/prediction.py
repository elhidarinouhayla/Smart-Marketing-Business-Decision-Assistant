from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional

class PredictionBase(BaseModel):
    predicted_rate: float
    confidence: float
    campaign_id: UUID

class PredictionCreate(PredictionBase):
    pass

class PredictionRead(PredictionBase):
    id: UUID
    
    model_config = ConfigDict(from_attributes=True)
