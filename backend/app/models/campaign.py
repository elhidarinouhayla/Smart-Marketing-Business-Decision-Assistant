from backend.app.db.database import Base
from sqlalchemy import String, Column, ForeignKey, Float, Enum, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum
import uuid

class CampaignStatus(str, enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Campaign(Base):
    __tablename__ = "campaigns"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    budget = Column(Float, nullable=False)  # budget: Decimal (Float mapped for simplicity if preferred, but usually Numeric)
    channel = Column(String, nullable=False)
    status = Column(Enum(CampaignStatus), default=CampaignStatus.DRAFT)
    
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    user = relationship("User", backref="campaigns")
    customers = relationship("Customer", back_populates="campaign")
    prediction = relationship("Prediction", back_populates="campaign", uselist=False)
    recommendations = relationship("Recommendation", back_populates="campaign")

    def create(self) -> bool:
        # Method placeholder
        return True
