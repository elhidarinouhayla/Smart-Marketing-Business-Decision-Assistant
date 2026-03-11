from backend.app.db.database import Base
from sqlalchemy import Column, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

class Recommendation(Base):
    __tablename__ = "recommendations"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    advice_text = Column(Text)
    campaign_id = Column(UUID(as_uuid=True), ForeignKey("campaigns.id"))
    
    # Relationship
    campaign = relationship("Campaign", back_populates="recommendations")

    def generateAdvice(self) -> None:
        # Method placeholder
        pass
