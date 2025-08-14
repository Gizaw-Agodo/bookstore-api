from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas.review import ReviewCreateModel
from app.models.review import Review
from uuid import UUID
from app.services.user_service import UserService
from app.services.book_service import BookService
from fastapi import HTTPException, status

class ReviewService():
    def __init__(self,user_service:UserService, book_service:BookService ):
        self.user_service = user_service
        self.book_service = book_service
    
    async def add_review_to_book(
            self, db : AsyncSession, 
            review_data:ReviewCreateModel,  
            book_id : UUID, 
            user_id : UUID
            ):
       
        user = await self.user_service.get_user_by_id(str(user_id), db)
        book = await self.book_service.get_book(db, str(book_id))

        if not user : 
            raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="User not found")
        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

        review_data_dict = review_data.model_dump()
        new_review = Review(**review_data_dict)
        new_review.book_id = book.id
        new_review.user_id = user.id

        db.add(new_review)
        await db.commit()
        await db.refresh(new_review)

        return new_review