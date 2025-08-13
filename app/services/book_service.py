from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from app.models.book import Book
from app.schemas.books import BookCreate, BookUpdate
from fastapi import HTTPException, status
from uuid import UUID

class BookService : 
    async def get_all_books(self, db: AsyncSession ):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await db.exec(statement)
        return result.all()
    
    async def get_book(self, db : AsyncSession, book_id : str): 
        statement = select(Book).where(Book.id == book_id)
        result = await db.exec(statement)
        return result.first()
    
    async def create_book(self, db : AsyncSession, book_data : BookCreate, user_id : UUID):
        book_data_dict = book_data.model_dump()
        new_book = Book(**book_data_dict)
        new_book.user_id = user_id
        db.add(new_book)
        await db.commit()
        return new_book
    
    async def update_book(self, db:AsyncSession, book_id:str, book_data :BookUpdate):
        update_data_dict = book_data.model_dump()
        book_to_update = await self.get_book(db, book_id)
        if not book_to_update : 
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Book not found")
        
        for key, value in update_data_dict.items():
            setattr(book_to_update, key, value)

        await db.commit()
        return book_to_update

    async def delete_book(self, db:AsyncSession, book_id : str):
        book_to_delete = await self.get_book(db, book_id)
        if not book_to_delete:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
        
        await db.delete(book_to_delete)
        await db.commit()



