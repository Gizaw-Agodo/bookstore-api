from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from app.models.user import User
from app.models.book import Book
from app.core.errors import NotFound
class UserService():

    async def get_user_by_email(self, email:str, db:AsyncSession):
        statement = select(User).where(User.email == email)
        result =  await db.exec(statement)

        user = result.first() 
        if not user:
            raise NotFound('User not found with that email ')
        
        return user
    
    async def get_user_by_id(self, id : str, db : AsyncSession):
        statement = select(User).where(User.id == id)
        user =  await db.exec(statement)
        return user.first()


    async def get_user_books(self, user_id : str , db : AsyncSession):
        statement = select(Book).where(Book.user_id == user_id).order_by(desc(Book.created_at))
        result = await db.exec(statement)
        return result.all()

    async def verify_user(self, email:str , db : AsyncSession):
        user = await self.get_user_by_email(email, db)
        user.is_verified = True
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

