from pydantic import BaseModel
from typing import Optional



# prediction
class PredictionRequest(BaseModel):
    campaign_id: str
    Age: int
    Income: float  
    WebsiteVisits: int
    SocialShares: int
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
    prediction: int     
    probability: float   
    message: str
    success: bool
    recommendation: Optional[str] = None
    
    class Config:
        from_attributes = True