from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.app.db.database import get_db
from backend.app.models.prediction import Prediction
from backend.app.models.campaign import Campaign
from backend.app.models.recommendation import Recommendation
from backend.app.schemas.prediction import PredictionRequest, PredictionResponse
from backend.app.schemas.recommendation import RecommendationResponse
from backend.app.authentification.auth import verify_token
from backend.app.services.ml_service import predict
from backend.app.services.gemini_service import retention_gemini
from typing import List

router = APIRouter(prefix="/predictions", tags=["Predictions"])


# ── Endpoint 1 : lancer une prediction ──
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
        message = "PREDICTION_SUCCES"
    else:
        message = "PREDICTION_ECHEC"

    new_prediction = Prediction(
        result=prediction_value,
        probability=probability,
        campaign_id=data.campaign_id
    )
    db.add(new_prediction)
    db.commit()
    db.refresh(new_prediction)

    return {
        "id": new_prediction.id,
        "campaign_id": new_prediction.campaign_id,
        "prediction": new_prediction.result,
        "probability": new_prediction.probability,
        "message": message,
        "success": prediction_value == 1
    }


# ── Endpoint 2 : generer le plan (appelle le 1er) ──
@router.post("/generate-plan", response_model=RecommendationResponse)
def generate_plan(data: PredictionRequest, db: Session = Depends(get_db), user: dict = Depends(verify_token)):
    print(f"[DEBUG] Generating plan for campaign {data.campaign_id}")
    try:
        # Appelle directement run_prediction
        prediction_result = run_prediction(data, db, user)
        probability = prediction_result["probability"]
        message = prediction_result["message"]
        success = prediction_result["success"]

        # Si succes → pas de plan requis (mais on doit respecter le schema RecommendationResponse)
        if success:
            print(f"[DEBUG] Campaign {data.campaign_id} is a success, no plan needed.")
            return {
                "id": "none",
                "campaign_id": data.campaign_id,
                "advice_text": "Aucun plan requis, la campagne a de bonnes chances de reussir"
            }

        # Si echec → Gemini genere le plan
        print(f"[DEBUG] Campaign {data.campaign_id} predicted to fail ({probability}). Triggering Gemini...")
        result_gemini = retention_gemini(probability, 0)
        advice_text = "\n".join(result_gemini.retention_plan)

        # Sauvegarder en base
        new_reco = Recommendation(
            advice_text=advice_text,
            campaign_id=data.campaign_id
        )
        db.add(new_reco)
        db.commit()
        db.refresh(new_reco)

        print(f"[DEBUG] Recommendation created with ID {new_reco.id}")
        return {
            "id": new_reco.id,
            "campaign_id": new_reco.campaign_id,
            "advice_text": advice_text
        }
    except Exception as e:
        print(f"[ERROR] generate_plan failed: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


# ── Historique des predictions ──
@router.get("/", response_model=List[PredictionResponse])
def get_predictions(db: Session = Depends(get_db), user: dict = Depends(verify_token)):
    predictions = db.query(Prediction).all()
    result = []
    for p in predictions:
        msg = "PREDICTION_SUCCES" if p.result == 1 else "PREDICTION_ECHEC"
        result.append({
            **p.__dict__,
            "prediction": p.result,
            "message": msg,
            "success": p.result == 1
        })
    return result


# ── Detail d'une prediction ──
@router.get("/{prediction_id}", response_model=PredictionResponse)
def get_prediction(prediction_id: str, db: Session = Depends(get_db), user: dict = Depends(verify_token)):
    p = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Prédiction non trouvée")

    msg = "PREDICTION_SUCCES" if p.result == 1 else "PREDICTION_ECHEC"
    return {
        **p.__dict__,
        "prediction": p.result,
        "message": msg,
        "success": p.result == 1
    }