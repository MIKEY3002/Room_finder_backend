from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    # The user who is reporting
    reporter_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # The house being reported
    boarding_house_id = Column(Integer, ForeignKey("boarding_houses.id"), nullable=False)
    
    # Predefined reason (e.g., "Scam", "Inaccurate Photos", "Sold/Unavailable")
    reason = Column(String, nullable=False)
    # Optional detailed description
    description = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())