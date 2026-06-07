from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.core.database import get_db
from app.models.user import User
from app.utils.supabase_auth import verify_token
from app.utils.token import SECRET_KEY, ALGORITHM

security = HTTPBearer()


def _verify_local_jwt(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    #  Check missing token
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing token"
        )

    payload = None
    try:
        payload = verify_token(token)
    except HTTPException:
        payload = _verify_local_jwt(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    email = payload.get("email") or payload.get("sub")

    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    email_verified = (
        payload.get("email_confirmed_at") is not None
        or payload.get("sub") is not None
    )

    if not email_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email not verified"
        )

    name = payload.get("user_metadata", {}).get("name", "New User")

    user = db.query(User).filter(User.email == email).first()

    if not user:
        user = User(
            email=email,
            name=name,
            password="supabase_auth",
            role="tenant",
            email_verified=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    elif not user.email_verified:
        user.email_verified = True
        db.commit()
        db.refresh(user)

    return user
