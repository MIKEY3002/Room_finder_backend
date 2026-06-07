from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.report import Report
from app.models.boarding_house import BoardingHouse
from app.schemas.report_schema import ReportCreate

def create_report(db: Session, house_id: int, reporter_id: int, data: ReportCreate):
    house = db.query(BoardingHouse).filter(BoardingHouse.id == house_id).first()
    if not house:
        raise HTTPException(status_code=404, detail="Boarding house not found")
    
    if house.owner_id == reporter_id:
        raise HTTPException(status_code=400, detail="You cannot report your own listing")

    new_report = Report(
        reporter_id=reporter_id,
        boarding_house_id=house_id,
        reason=data.reason,
        description=data.description
    )
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    return new_report


def get_reports(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Report).offset(skip).limit(limit).all()