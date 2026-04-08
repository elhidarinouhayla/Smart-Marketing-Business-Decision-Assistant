import uuid
from sqlalchemy import Column, String, Integer, Float
from backend.app.db.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    age = Column(Integer, nullable=False)
    income = Column(Float, nullable=False)
    segment_label = Column(String, nullable=True)  