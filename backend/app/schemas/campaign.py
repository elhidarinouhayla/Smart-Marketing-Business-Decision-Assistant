from pydantic import BaseModel, ConfigDict
from uuid import UUID
from enum import Enum
from typing import Optional, List

class CampaignStatusEnum(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class CampaignBase(BaseModel):
    name: str
    budget: float
    channel: str
    status: CampaignStatusEnum = CampaignStatusEnum.DRAFT

class CampaignCreate(CampaignBase):
    user_id: int

class CampaignRead(CampaignBase):
    id: UUID
    user_id: int
    
    model_config = ConfigDict(from_attributes=True)
