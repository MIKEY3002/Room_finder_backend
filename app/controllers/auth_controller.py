from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.user_schema import UserCreate, UserLogin, UserResponse, TokenResponse
from app.core.database import get_db
from app.middleware.auth_middleware import get_current_user
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])


# REGISTER
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    return auth_service.create_user(db, user_data)


# LOGIN
@router.post("/login", response_model=TokenResponse)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    token_data = auth_service.login_user(db, user_data.email, user_data.password)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    return token_data


# PROFILE (Protected)
@router.get("/users/profile", response_model=UserResponse)
def get_profile(current_user = Depends(get_current_user)):
    return current_user
