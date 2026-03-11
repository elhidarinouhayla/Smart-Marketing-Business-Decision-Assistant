from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional

class RecommendationBase(BaseModel):
    advice_text: str
    campaign_id: UUID

class RecommendationCreate(RecommendationBase):
    pass

class RecommendationRead(RecommendationBase):
    id: UUID
    
    model_config = ConfigDict(from_attributes=True)
