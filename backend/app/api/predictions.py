from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.app.db.database import get_db
from backend.app.models.prediction import Prediction
from backend.app.models.campaign import Campaign
from backend.app.schemas.schemas import PredictionRequest, PredictionResponse
from backend.app.authentification.auth import verify_token
from backend.app.services.ml_service import predict 
from typing import List

router = APIRouter(prefix="/predictions", tags=["Predictions"])


# lancer une prediction pour une campagne
@router.post("/", response_model=PredictionResponse)
def run_prediction(data: PredictionRequest, db: Session = Depends(get_db), user: dict = Depends(verify_token)):

    # verifier que la campagne existe
    campaign = db.query(Campaign).filter(Campaign.id == data.campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campagne non trouvée")

    features = data.model_dump(exclude={"campaign_id"})

    result = predict(features)

    probability = result["probability"]
    prediction_value = result["prediction"]

  
    if probability < 0.40:
        message = "La campagne a peu de chances de réussir"
    elif probability < 0.70:
        message = "La campagne peut être améliorée"
    else:
        message = "La campagne est efficace mais peut être optimisée"

    # Sauvegarder en base
    new_prediction = Prediction(
        predicted_rate=probability,
        confidence=probability,   
        campaign_id=data.campaign_id
    )
    db.add(new_prediction)
    db.commit()
    db.refresh(new_prediction)

    return {
        "id": new_prediction.id,
        "campaign_id": new_prediction.campaign_id,
        "predicted_rate": new_prediction.predicted_rate,
        "confidence": new_prediction.confidence,
        "message": message
    }


# historique des predictions
@router.get("/", response_model=List[PredictionResponse])
def get_predictions(db: Session = Depends(get_db), user: dict = Depends(verify_token)):
    predictions = db.query(Prediction).all()
    result = []
    for p in predictions:
        if p.predicted_rate < 0.40:
            msg = "La campagne a peu de chances de réussir"
        elif p.predicted_rate < 0.70:
            msg = "La campagne peut être améliorée"
        else:
            msg = "La campagne est efficace mais peut être optimisée"
        result.append({**p.__dict__, "message": msg})
    return result


# detail d'une prediction 
@router.get("/{prediction_id}", response_model=PredictionResponse)
def get_prediction(prediction_id: str, db: Session = Depends(get_db), user: dict = Depends(verify_token)):
    p = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Prédiction non trouvée")

    if p.predicted_rate < 0.40:
        msg = "La campagne a peu de chances de réussir"
    elif p.predicted_rate < 0.70:
        msg = "La campagne peut être améliorée"
    else:
        msg = "La campagne est efficace mais peut être optimisée"

    return {**p.__dict__, "message": msg}