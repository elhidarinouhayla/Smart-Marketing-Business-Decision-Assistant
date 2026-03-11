from backend.app.db.database import Base
from sqlalchemy import Column, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    predicted_rate = Column(Float)
    confidence = Column(Float)
    campaign_id = Column(UUID(as_uuid=True), ForeignKey("campaigns.id"))
    
    # Relationship
    campaign = relationship("Campaign", back_populates="prediction")

    def runInference(self) -> None:
        # Method placeholder
        pass
