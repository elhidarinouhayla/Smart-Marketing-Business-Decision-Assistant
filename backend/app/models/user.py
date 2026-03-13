from backend.app.db.database import Base
from sqlalchemy import String, Integer, Column, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False )
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at= Column(DateTime, default= datetime.now )

    # Relationships
    campaigns = relationship("Campaign", back_populates="user")