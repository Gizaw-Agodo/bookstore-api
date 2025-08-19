from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas.auth import UserCreate, UserLoginModel
from app.models.user import User
from app.core.security import hash_password, verify_password
from app.core.security import create_refresh_token, create_token
from app.services.user_service import UserService
from typing import  Any
from app.core.errors import BadRequest, InternalServerError
from sqlalchemy.exc import SQLAlchemyError
from app.core.errors import Unauthorized
from app.schemas.auth import ResetPasswordModel


class AuthService:
    def __init__(self, user_service : UserService):
        self.user_service = user_service

    
    async def create_user(self, db : AsyncSession, user_data: UserCreate):
        existing_user = await self.user_service.get_user_by_email(user_data.email, db)
        if existing_user :
            raise BadRequest("User With The Email Exists")
       
        try : 
            user_dict = user_data.model_dump()
            new_user = User(**user_dict)
            new_user.password_hash = hash_password(user_data.password)
            new_user.role = "user"
            db.add(new_user)
            await db.commit()
            return new_user
    
        except SQLAlchemyError:
            await db.rollback()
            raise InternalServerError("A database error occurred during user creation.")
        except:
            await db.rollback()
            raise InternalServerError("An unexpected error occurred during user creation.")
        
        
        
    
    async def login(self, db : AsyncSession, login_data : UserLoginModel) -> dict[str, Any] :
        
        user = await self.user_service.get_user_by_email(login_data.email, db)
        if not user:
            raise Unauthorized("User not found")
        
        is_password_valid = verify_password(user.password_hash, login_data.password)
        if not is_password_valid:
            raise Unauthorized("Invalid credentials provided")
        
        access_token = create_token({"email" : user.email,"id" : str(user.id), "role" : user.role})
        refresh_token = create_refresh_token({"email" : user.email,"id" : str(user.id)})
        return {
            "user": user,
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    
    async def reset_password(self, email:str, data :ResetPasswordModel,  db:AsyncSession):

        if data.confirm_password != data.new_password:
            raise BadRequest('Password do not match')
        
        user = await self.user_service.get_user_by_email(email, db)
        user.password_hash = hash_password(data.new_password)

        try:
            db.add(user)
            await db.commit()
            await db.refresh(user)
        except : 
            InternalServerError("Internal server errr")



       
            