from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.favorite import Favorite
from app.models.boarding_house import BoardingHouse


def toggle_favorite(db: Session, user_id: int, house_id: int):
    existing_favorite = db.query(Favorite).filter(
        Favorite.user_id == user_id,
        Favorite.house_id == house_id
    ).first()

    if existing_favorite:
        db.delete(existing_favorite)
        db.commit()
        return {"message": "Favorite removed"}

    house = db.query(BoardingHouse).filter(BoardingHouse.id == house_id).first()
    if not house:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Boarding house not found"
        )

    favorite = Favorite(user_id=user_id, house_id=house_id)
    db.add(favorite)
    db.commit()
    db.refresh(favorite)
    return {"message": "Added to favorites"}


def get_user_favorites(db: Session, user_id: int):
    favorites = db.query(Favorite).filter(Favorite.user_id == user_id).all()
    house_list = []
    for favorite in favorites:
        if favorite.boarding_house:
            house = favorite.boarding_house
            house_list.append({
                "id": house.id,
                "title": house.title,
                "description": house.description,
                "price": house.price,
                "address": house.address,
                "barangay": house.barangay,
                "city": house.city,
                "province": house.province,
                "country": house.country,
                "latitude": house.latitude,
                "longitude": house.longitude,
                "wifi_available": house.wifi_available,
                "beds": house.beds,
                "is_available": house.is_available,
                "gender_allowed": house.gender_allowed,
                "owner_id": house.owner_id,
                "created_at": house.created_at,
                "updated_at": house.updated_at,
            })
    return house_list
