from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.app.db.database import get_db
from backend.app.models.prediction import Prediction
from backend.app.models.campaign import Campaign
from backend.app.models.recommendation import Recommendation
from backend.app.schemas.prediction import PredictionRequest, PredictionResponse
from backend.app.authentification.auth import verify_token
from backend.app.services.ml_service import predict
from backend.app.services.gemini_service import retention_gemini
from typing import List

router = APIRouter(prefix="/predictions", tags=["Predictions"])


# lancer une prediction pour une campagne
@router.post("/", response_model=PredictionResponse)
def run_prediction(data: PredictionRequest, db: Session = Depends(get_db), user: dict = Depends(verify_token)):

    campaign = db.query(Campaign).filter(Campaign.id == data.campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campagne non trouvée")

    features = data.model_dump(exclude={"campaign_id"})
    result = predict(features)

    prediction_value = int(result["prediction"])
    probability = float(result["probability"])

    if prediction_value == 1:
        message = "La campagne a de bonnes chances de reussir"
    else:
        message = "La campagne a peu de chances de reussir"

    new_prediction = Prediction(
        result=prediction_value,
        probability=probability,
        campaign_id=data.campaign_id
    )
    db.add(new_prediction)

    # Generate automatic recommendation
    advice_text = None
    try:
        reco_result = retention_gemini(probability, prediction_value)
        advice_text = "\n".join(reco_result.retention_plan)

        new_reco = Recommendation(
            advice_text=advice_text,
            campaign_id=data.campaign_id
        )
        db.add(new_reco)
    except Exception as e:
        print(f"Error generating automatic recommendation: {e}")
        # advice_text remains None if an error occurs

    db.commit()
    db.refresh(new_prediction)

    return {
        "id": new_prediction.id,
        "campaign_id": new_prediction.campaign_id,
        "prediction": new_prediction.result,
        "probability": new_prediction.probability,
        "message": message,
        "success": prediction_value == 1,
        "recommendation": advice_text
    }


# historique des predictions
@router.get("/", response_model=List[PredictionResponse])
def get_predictions(db: Session = Depends(get_db), user: dict = Depends(verify_token)):
    predictions = db.query(Prediction).all()
    result = []
    for p in predictions:
        msg = "La campagne a de bonnes chances de reussir" if p.result == 1 else "La campagne a peu de chances de reussir"
        result.append({
            **p.__dict__,
            "prediction": p.result,
            "message": msg,
            "success": p.result == 1
        })
    return result


# detail d'une prediction
@router.get("/{prediction_id}", response_model=PredictionResponse)
def get_prediction(prediction_id: str, db: Session = Depends(get_db), user: dict = Depends(verify_token)):
    p = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Prédiction non trouvée")

    msg = "La campagne a de bonnes chances de reussir" if p.result == 1 else "La campagne a peu de chances de reussir"
    return {
        **p.__dict__,
        "prediction": p.result,
        "message": msg,
        "success": p.result == 1
    }