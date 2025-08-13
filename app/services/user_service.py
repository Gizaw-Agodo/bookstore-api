from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from app.models.user import User
from app.models.book import Book

class UserService():

    async def get_user_by_email(self, email:str, db:AsyncSession):
        statement = select(User).where(User.email == email)
        user =  await db.exec(statement)
        return user.first()

    async def get_user_books(self, user_id : str , db : AsyncSession):
        statement = select(Book).where(Book.user_id == user_id).order_by(desc(Book.created_at))
        result = await db.exec(statement)
        return result.all()
