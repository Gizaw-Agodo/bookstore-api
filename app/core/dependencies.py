from app.services.book_service import BookService
from app.services.auth_service import AuthService
from app.models.user import User
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.database import get_session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.security import verify_access_token
 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login ')

def get_book_service() -> BookService:
    return BookService()

def get_auth_service() -> AuthService:
    return AuthService()

async def get_current_user(
    db: AsyncSession = Depends(get_session),
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
) -> User:
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    email: str | None = payload.get("email")  # type: ignore

    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    user = await auth_service.get_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user
