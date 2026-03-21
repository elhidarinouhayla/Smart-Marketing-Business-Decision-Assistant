import uuid
from sqlalchemy import Column, String, Float, ForeignKey, Integer
from backend.app.db.database import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    result = Column(Integer, nullable=False)
    probability = Column(Float, nullable=False)
    campaign_id = Column(String, ForeignKey("campaigns.id"), nullable=False)