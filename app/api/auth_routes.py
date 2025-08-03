from fastapi import APIRouter, Depends, status
from app.schemas.auth import UserCreate
from app.core.dependencies import get_auth_service
from app.services.auth_service import AuthService
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.database import get_session


auth_router = APIRouter()

@auth_router.post('/signup', status_code=status.HTTP_201_CREATED)
async def create_user_account(
    user_data : UserCreate,  
    auth_service:AuthService =  Depends(get_auth_service), 
    db: AsyncSession  =  Depends(get_session)
):
    new_user = await auth_service.create_user(db, user_data)
    return new_user
