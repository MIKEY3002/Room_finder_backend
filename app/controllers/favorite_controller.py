from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.middleware.auth_middleware import get_current_user
from app.services.favorite_service import toggle_favorite, get_user_favorites

router = APIRouter(prefix="/favorites", tags=["Favorites"])

@router.post("/{house_id}")
def toggle(house_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return toggle_favorite(db, current_user.id, house_id)

@router.get("/")
def get_favorites(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # Returns a list of favorited houses for the logged-in user
    return get_user_favorites(db, current_user.id)