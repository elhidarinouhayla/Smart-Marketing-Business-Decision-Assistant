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


# prediction
class PredictionRequest(BaseModel):
    campaign_id: str
    Gender: str
    CampaignChannel: str
    CampaignType: str
    AdvertisingPlatform: str
    AdvertisingTool: str
    SegmentName: str
    AdSpend: float
    ClickThroughRate: float
    PagesPerVisit: float
    TimeOnSite: float
    EmailOpens: int
    EmailClicks: int
    PreviousPurchases: int
    LoyaltyPoints: int

class PredictionResponse(BaseModel):
    id: str
    campaign_id: str
    predicted_rate: int       
    confidence: float            
    message: str                 

    class Config:
        from_attributes = True


# recommandation
class RecommendationRequest(BaseModel):
    campaign_id: str
    probability: float          
    prediction: int          

class RecommendationResponse(BaseModel):
    id: str
    campaign_id: str
    advice_text: str             

    class Config:
        from_attributes = True


# dashboard
class DashboardResponse(BaseModel):
    total_campaigns: int
    active_campaigns: int
    avg_predicted_rate: float
    total_customers: int
    total_segments: int