from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.db.database import get_db
from backend.app.models.campaign import Campaign
from backend.app.models.customer import Customer
from backend.app.models.prediction import Prediction
from backend.app.schemas.dashboards import DashboardResponse
from backend.app.authentification.auth import verify_token

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/overview", response_model=DashboardResponse)
def get_overview(db: Session = Depends(get_db), user: dict = Depends(verify_token)):
    print(f"[DEBUG] Fetching overview for user {user.get('id')}")
    try:
        campaigns = db.query(Campaign).filter(Campaign.user_id == user["id"]).all()
        active_campaigns = [c for c in campaigns if c.status == "active"]

        predictions = db.query(Prediction).all()
        avg_rate = round(sum(p.probability for p in predictions) / len(predictions), 2) if predictions else 0.0

        customers = db.query(Customer).all()
        segments = set(c.segment_label for c in customers if c.segment_label)

        return {
            "total_campaigns": len(campaigns),
            "active_campaigns": len(active_campaigns),
            "avg_predicted_rate": avg_rate,
            "total_customers": len(customers),
            "total_segments": len(segments)
        }
    except Exception as e:
        print(f"[ERROR] get_overview failed: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))