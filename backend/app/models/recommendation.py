import uuid
from sqlalchemy import Column, String, Text, ForeignKey
from backend.app.db.database import Base


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    advice_text = Column(Text, nullable=False)  # texte généré par Gemini
    campaign_id = Column(String, ForeignKey("campaigns.id"), nullable=False)