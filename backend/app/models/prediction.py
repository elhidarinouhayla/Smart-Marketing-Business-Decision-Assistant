import uuid
from sqlalchemy import Column, String, Float, ForeignKey
from backend.app.db.database import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    predicted_rate = Column(Float, nullable=False)   # ex: 0.72
    confidence = Column(Float, nullable=False)        # ex: 0.89
    campaign_id = Column(String, ForeignKey("campaigns.id"), nullable=False)