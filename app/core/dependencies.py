from app.services.book_service import BookService
from app.services.auth_service import AuthService
from app.models.user import User
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.database import get_session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.security import verify_access_token
from app.core.redis import token_in_blocklist
from app.services.user_service import UserService
from app.services.review_service import ReviewService
 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login ')

def get_book_service() -> BookService:
    return BookService()

def get_user_service() -> UserService:
    return UserService()

def get_auth_service(user_service :UserService = Depends(get_user_service) ) -> AuthService:
    return AuthService(user_service)

def get_review_service(
        user_service:UserService = Depends(get_user_service), 
        book_service : BookService= Depends(get_book_service)
        ):
    return  ReviewService(user_service, book_service)

async def get_current_user(
    db: AsyncSession = Depends(get_session),
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(get_user_service),
) -> User:
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    
    jti : str | None = payload.get('jti')

    if jti is None : 
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail='Invalid token : Missing JTI', headers={"WWW-Authenticate" : "Bearer"})
    
    is_token_in_block_list = await token_in_blocklist(jti)
    if is_token_in_block_list: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has been revoked", headers= {"WWW-Authenticate" : "Bearer"})

    email: str | None = payload.get("email") 
    

    if not email:
        raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token", headers={"WWW-Authenticate" : "Bearer"})

    user = await user_service.get_user_by_email(email,db)
    if not user:
        raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found", headers= {"WWW-Authenticate" : "Bearer"})

    return user
