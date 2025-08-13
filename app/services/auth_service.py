from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas.auth import UserCreate, UserLoginModel
from app.models.user import User
from fastapi import HTTPException, status
from app.core.security import hash_password, verify_password
from app.core.security import create_refresh_token, create_token
from app.services.user_service import UserService
from typing import  Any


class AuthService:
    def __init__(self, user_service : UserService):
        self.user_service = user_service

    
    async def create_user(self, db : AsyncSession, user_data: UserCreate):
        existing_user = await self.user_service.get_user_by_email(user_data.email, db)
        if existing_user :
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user with the email exist")
       
        
        user_dict = user_data.model_dump()
        new_user = User(**user_dict)
        new_user.password_hash = hash_password(user_data.password)
        new_user.role = "user"
        db.add(new_user)
        await db.commit()
        return new_user
    
    async def login(self, db : AsyncSession, login_data : UserLoginModel) -> dict[str, Any] :
        user = await self.user_service.get_user_by_email(login_data.email, db)
            
        if user is not None : 
            is_password_valid = verify_password(user.password_hash, login_data.password)
            if is_password_valid:
                access_token = create_token({"email" : user.email,"id" : str(user.id), "role" : user.role})
                refresh_token = create_refresh_token({"email" : user.email,"id" : str(user.id)})
                return {
                    "user": user,
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }
            else: 
                raise HTTPException(detail='user not found', status_code=status.HTTP_401_UNAUTHORIZED)  
        else:
            raise HTTPException(detail='user not found', status_code=status.HTTP_401_UNAUTHORIZED)  
                

            
            