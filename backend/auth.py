"""JWT authentication and role-based access control."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from pydantic import BaseModel

from .config import settings


security = HTTPBearer()


class TokenData(BaseModel):
    """JWT token payload."""
    sub: str  # user ID
    role: str  # "faculty", "student", "admin"
    course_id: Optional[str] = None
    exp: datetime


def create_access_token(
    subject: str,
    role: str,
    course_id: Optional[str] = None,
    expires_delta: Optional[timedelta] = None
) -> str:
    """Create JWT access token."""
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.access_token_expire_minutes)

    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {
        "sub": subject,
        "role": role,
        "course_id": course_id,
        "exp": expire,
    }

    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm
    )
    return encoded_jwt


async def verify_token(
    credentials: HTTPAuthCredentials = Depends(security),
) -> TokenData:
    """Verify JWT token and return token data."""
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        user_id: str = payload.get("sub")
        role: str = payload.get("role")
        course_id: Optional[str] = payload.get("course_id")

        if user_id is None or role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        return TokenData(
            sub=user_id,
            role=role,
            course_id=course_id,
            exp=datetime.fromtimestamp(payload.get("exp"))
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


async def get_current_user(
    token_data: TokenData = Depends(verify_token)
) -> TokenData:
    """Get current authenticated user."""
    return token_data


async def require_role(role: str):
    """Dependency: require specific role."""
    async def _check_role(current_user: TokenData = Depends(get_current_user)) -> TokenData:
        if current_user.role != role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"This endpoint requires {role} role"
            )
        return current_user
    return _check_role
