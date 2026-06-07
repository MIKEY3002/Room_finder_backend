from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.middleware.auth_middleware import get_current_user

from app.schemas.review_schema import ReviewCreate, ReviewResponse
from app.services.review_service import create_review, get_reviews_by_house
from app.schemas.review_schema import ReviewUpdate
from app.services.review_service import create_review, update_review

router = APIRouter(prefix="/reviews", tags=["Reviews"])


#  Create Review
@router.post("/", response_model=ReviewResponse)
def add_review(
    data: ReviewCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return create_review(db, data, current_user.id)

@router.put("/{review_id}")
def edit_review(
    review_id: int,
    data: ReviewUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return update_review(
        db=db,
        review_id=review_id,
        user_id=current_user.id,
        rating=data.rating,
        comment=data.comment
    )


#  Get Reviews per Boarding House
@router.get("/{house_id}", response_model=list[ReviewResponse])
def get_reviews(house_id: int, db: Session = Depends(get_db)):
    return get_reviews_by_house(db, house_id)