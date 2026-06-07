from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReportCreate(BaseModel):
    reason: str
    description: Optional[str] = None

class ReportResponse(ReportCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True