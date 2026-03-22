import sys
import os

# Set project root
project_root = "/home/nouhayla/Desktop/simplon_projects/smart_marketing/Smart-Marketing-Business-Decision-Assistant/"
sys.path.append(project_root)

from backend.app.db.database import SessionLocal, Base, engine
from backend.app.models.user import User
from backend.app.models.campaign import Campaign
from backend.app.models.prediction import Prediction
from backend.app.models.recommendation import Recommendation
from backend.app.models.customer import Customer
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def populate():
    db = SessionLocal()
    try:
        # 1. Create Test User
        user = db.query(User).filter(User.username == "testuser").first()
        if not user:
            user = User(username="testuser", email="test@example.com", password=pwd_context.hash("testpassword123"))
            db.add(user)
            db.commit()
            db.refresh(user)

        # 2. Add Campaigns
        campaigns = db.query(Campaign).filter(Campaign.user_id == user.id).all()
        if not campaigns:
            campaigns = [
                Campaign(name="Social Media Summer", budget=500.0, channel="Social Media", status="active", user_id=user.id),
                Campaign(name="Email Blast Fall", budget=300.0, channel="Email", status="active", user_id=user.id),
                Campaign(name="PPC Winter", budget=1000.0, channel="PPC", status="paused", user_id=user.id),
                Campaign(name="SEO Campaign", budget=200.0, channel="SEO", status="inactive", user_id=user.id),
            ]
            db.add_all(campaigns)
            db.commit()
            # No refresh needed for lists, but we need IDs for predictions
        
        # 3. Add Predictions
        if db.query(Prediction).count() == 0:
            campaigns = db.query(Campaign).filter(Campaign.user_id == user.id).all()
            if campaigns:
                preds = [
                    Prediction(result=1, probability=0.85, campaign_id=campaigns[0].id),
                    Prediction(result=1, probability=0.72, campaign_id=campaigns[1].id),
                    Prediction(result=0, probability=0.45, campaign_id=campaigns[2].id)
                ]
                db.add_all(preds)
                db.commit()

        # 4. Add Recommendations
        if db.query(Recommendation).count() == 0:
            campaigns = db.query(Campaign).filter(Campaign.user_id == user.id).all()
            if campaigns:
                recos = [
                    Recommendation(advice_text="Augmenter le budget Social Media pour la cible senior.", campaign_id=campaigns[0].id),
                    Recommendation(advice_text="Optimiser les heures d'envoi d'emails le mardi à 10h.", campaign_id=campaigns[1].id),
                ]
                db.add_all(recos)
                db.commit()
            
        # 5. Add Customers
        if db.query(Customer).count() == 0:
            custs = [Customer(age=34, income=65000, segment_label="Premium") for _ in range(50)]
            db.add_all(custs)
            db.commit()

        print("DB populated for testuser successfully.")
    except Exception as e:
        print(f"Error populating DB: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    populate()
