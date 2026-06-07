from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.middleware.auth_middleware import get_current_user
from app.schemas.report_schema import ReportCreate, ReportResponse
from app.services.report_service import create_report
from app.services.boarding_house_service import get_my_boarding_houses

from app.schemas.boarding_house_schema import (
    BoardingHouseCreate,
    BoardingHouseResponse,
)
from app.services.boarding_house_service import (
    create_boarding_house,
    get_all_boarding_houses,
    get_boarding_house_by_id,
    update_boarding_house,
    delete_boarding_house,
    update_boarding_house_availability,
    get_featured_boarding_houses,
)

router = APIRouter(prefix="/boarding-houses", tags=["Boarding Houses"])


#  CREATE
@router.post("/", response_model=BoardingHouseResponse)
def create_house(
    data: BoardingHouseCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return create_boarding_house(db, data, current_user.id)

@router.get("/my/")
def my_boarding_houses(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_my_boarding_houses(db, current_user.id)



#  GET ALL + FILTER
@router.get("/", response_model=list[BoardingHouseResponse])
def get_all_houses(
    db: Session = Depends(get_db),
    search: Optional[str] = Query(None),
    max_price: Optional[float] = Query(None),
    wifi: Optional[bool] = Query(None),
    gender: Optional[list[str]] = Query(None),
    barangay: Optional[str] = Query(None),
    city: Optional[str] = Query(None),
    province: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
):
    # The service now returns BoardingHouseResponse objects directly,
    # including the average_rating and new fields.
    return get_all_boarding_houses(
        db, search, max_price, wifi, gender, barangay, city, province, skip, limit
    )


#  GET FEATURED
@router.get("/featured/", response_model=list[BoardingHouseResponse])
def get_featured_houses(
    db: Session = Depends(get_db),
    limit: int = Query(5, ge=1, le=10),
):
    return get_featured_boarding_houses(db, limit)


#  GET SINGLE
@router.get("/{id}", response_model=BoardingHouseResponse)
def get_single_house(
    id: int,
    db: Session = Depends(get_db)
):
    house = get_boarding_house_by_id(db, id)

    if not house:
        raise HTTPException(status_code=404, detail="Boarding house not found")
    
    # The service now returns a BoardingHouseResponse object directly
    return house


#  UPDATE
@router.put("/{id}", response_model=BoardingHouseResponse)
def update_house(
    id: int,
    data: BoardingHouseCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = update_boarding_house(db, id, data, current_user.id)

    if result is None:
        raise HTTPException(status_code=404, detail="Boarding house not found")

    if result == "unauthorized":
        raise HTTPException(status_code=403, detail="Not allowed")

    return result


# TOGGLE AVAILABILITY
@router.patch("/{id}/availability", response_model=BoardingHouseResponse)
def toggle_availability(
    id: int,
    data: dict,  # Expecting {"is_available": bool}
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    is_available = data.get("is_available")
    if is_available is None:
        raise HTTPException(status_code=400, detail="is_available field required")
        
    result = update_boarding_house_availability(db, id, current_user.id, is_available)
    if result is None:
        raise HTTPException(status_code=404, detail="Boarding house not found")
    if result == "unauthorized":
        raise HTTPException(status_code=403, detail="Not allowed")
    return result


#  DELETE
@router.delete("/{id}")
def delete_house(
    id: int,
    confirmation_name: str = Query(..., description="Must match the boarding house title"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = delete_boarding_house(db, id, current_user.id, confirmation_name)

    if result is None:
        raise HTTPException(status_code=404, detail="Boarding house not found")

    if result == "unauthorized":
        raise HTTPException(status_code=403, detail="Not allowed")
        
    if result == "name_mismatch":
        raise HTTPException(status_code=400, detail="Confirmation name does not match the house title")

    return {"message": "Boarding house deleted successfully"}

# REPORT LISTING
@router.post("/{id}/report", response_model=ReportResponse)
def report_house(
    id: int,
    data: ReportCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return create_report(db, id, current_user.id, data)
