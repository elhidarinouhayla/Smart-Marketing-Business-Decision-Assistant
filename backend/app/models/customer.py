from backend.app.db.database import Base
from sqlalchemy import String, Integer, Column, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

class Customer(Base):
    __tablename__ = "customers"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    age = Column(Integer)
    income = Column(Float)
    segment_label = Column(String)
    campaign_id = Column(UUID(as_uuid=True), ForeignKey("campaigns.id"))
    
    # Relationship
    campaign = relationship("Campaign", back_populates="customers")

    def applyClustering(self) -> None:
        # Method placeholder
        pass
