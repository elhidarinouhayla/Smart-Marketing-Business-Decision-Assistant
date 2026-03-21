from pydantic import BaseModel
from typing import Optional

# campaign
class CampaignCreate(BaseModel):
    name: str
    budget: float
    channel: str
    status: str = "draft"

class CampaignUpdate(BaseModel):
    name: Optional[str] = None
    budget: Optional[float] = None
    channel: Optional[str] = None
    status: Optional[str] = None

class CampaignResponse(BaseModel):
    id: str
    name: str
    budget: float
    channel: str
    status: str
    user_id: int

    class Config:
        from_attributes = True