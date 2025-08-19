from app.services.book_service import BookService
from app.services.auth_service import AuthService
from app.models.user import User
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.database import get_session
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from app.core.security import verify_access_token
from app.core.redis import token_in_blocklist
from app.services.user_service import UserService
from app.services.review_service import ReviewService
from app.core.errors import Unauthorized
from app.services.email_service import EmailService
 

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

def get_email_service() -> EmailService:
    return EmailService()

async def get_current_user(
    db: AsyncSession = Depends(get_session),
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(get_user_service),
) -> User:
    payload = verify_access_token(token)
    if not payload:
        raise Unauthorized("Invalid or expired token")
    
    jti : str | None = payload.get('jti')
    if jti is None : 
        raise Unauthorized("Invalid token: Missing JTI")
    
    is_token_in_block_list = await token_in_blocklist(jti)
    if is_token_in_block_list: 
        raise Unauthorized("Token has been revoked")

    email: str | None = payload.get("email") 
    if not email:
        raise Unauthorized("Invalid or expired token")

    user = await user_service.get_user_by_email(email,db)
    if not user:
        raise Unauthorized("User not found")
    return user
