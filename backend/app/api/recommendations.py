from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.app.db.database import get_db
from backend.app.models.recommendation import Recommendation
from backend.app.models.campaign import Campaign
from backend.app.schemas.schemas import RecommendationRequest, RecommendationResponse
from backend.app.authentification.auth import verify_token
from backend.app.services.gemini_service import retention_gemini   
from typing import List
import json

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


# generer une recommandation 
@router.post("/generate", response_model=RecommendationResponse)
def generate_recommendation(data: RecommendationRequest, db: Session = Depends(get_db), user: dict = Depends(verify_token)):

    # verifier que la campagne existe
    campaign = db.query(Campaign).filter(Campaign.id == data.campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campagne non trouvée")


    result = retention_gemini(data.probability, data.prediction)

    advice_text = "\n".join(result.retention_plan)

    # Sauvegarder en base
    new_reco = Recommendation(
        advice_text=advice_text,
        campaign_id=data.campaign_id
    )
    db.add(new_reco)
    db.commit()
    db.refresh(new_reco)

    return new_reco


# historique des recommandations
@router.get("/", response_model=List[RecommendationResponse])
def get_recommendations(db: Session = Depends(get_db), user: dict = Depends(verify_token)):
    return db.query(Recommendation).all()