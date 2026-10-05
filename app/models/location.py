import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from app.database.base import Base

class Location(Base):
    __tablename__ = "locations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), nullable=False, unique=True, index=True)
    city = Column(String(50), nullable=False)
    state = Column(String(2), nullable=False)
    # maybe someday...
    # country = Column(String(50), nullable=False, default="BR")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)