from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas.auth import UserCreate
from app.models.user import User
from sqlmodel import select
from fastapi import HTTPException, status
from app.core.security import hash_password

class AuthService:
    async def get_user(self, db : AsyncSession, email  : str): 
        statement = select(User).where(User.email == email)
        user = await db.exec(statement)
        return user.first()
    async def get_user_by_email(self, db:AsyncSession, email : str): 
        statement = select(User).where(User.email == email)
        user =  await db.exec(statement)
        return user.first()
    
    async def create_user(self, db : AsyncSession, user_data: UserCreate):
        existing_user = await self.get_user(db, user_data.email)
        if existing_user :
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user with the email exist")
        
        user_dict = user_data.model_dump()
        new_user = User(**user_dict)
        new_user.password_hash = hash_password(user_data.password)
        db.add(new_user)
        await db.commit()
        return new_user
            

    

            
            

        
        