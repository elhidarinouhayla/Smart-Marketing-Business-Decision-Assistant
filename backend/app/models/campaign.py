import uuid
from sqlalchemy import Column, String, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship
from backend.app.db.database import Base


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    budget = Column(Float, nullable=False)
    channel = Column(String, nullable=False)
    status = Column(String, default="draft")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="campaigns")  # ← "campaigns" pas "user"