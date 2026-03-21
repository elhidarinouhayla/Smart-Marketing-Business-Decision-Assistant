from pydantic import BaseModel
from typing import Optional



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