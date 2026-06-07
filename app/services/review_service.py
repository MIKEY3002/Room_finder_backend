from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from fastapi import HTTPException, status

from app.models.review import Review
from app.schemas.review_schema import ReviewCreate
from fastapi import HTTPException, status


def create_review(db: Session, data: ReviewCreate, user_id: int):
    new_review = Review(
        rating=data.rating,
        comment=data.comment,
        user_id=user_id,
        boarding_house_id=data.boarding_house_id
    )

    db.add(new_review)

    try:
        db.commit()
        db.refresh(new_review)
        return new_review

    except IntegrityError:
        db.rollback()  #  REQUIRED after failed commit
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You already reviewed this boarding house"
        )


def get_reviews_by_house(db: Session, house_id: int):
    return db.query(Review).filter(
        Review.boarding_house_id == house_id
    ).all()


def get_average_rating(db: Session, house_id: int):
    avg = db.query(func.avg(Review.rating)).filter(
        Review.boarding_house_id == house_id
    ).scalar()

    return round(avg, 1) if avg else 0

def update_review(
    db: Session,
    review_id: int,
    user_id: int,
    rating: int,
    comment: str | None = None
):
    review = db.query(Review).filter(
        Review.id == review_id
    ).first()

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )

    #  Ownership check
    if review.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to edit this review"
        )

    #  Update fields
    review.rating = rating
    review.comment = comment

    db.commit()
    db.refresh(review)

    return review