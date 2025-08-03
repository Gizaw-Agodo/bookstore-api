from fastapi import APIRouter, status, Depends
from typing import List 
from app.models.book import Book
from app.services.book_service import BookService
from app.core.dependencies import get_book_service
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.database import get_session
from app.schemas.books import BookCreate, BookUpdate

book_router = APIRouter()

@book_router.get('/', response_model=List[Book], status_code= status.HTTP_200_OK)
async def get_books(
    book_service : BookService = Depends(get_book_service),
    db : AsyncSession = Depends(get_session)
    ):
        books = await book_service.get_all_books(db)
        return books

@book_router.get('/{book_id}', response_model=Book , status_code= status.HTTP_200_OK)
async def get_book(
    book_id : str,
    book_service : BookService = Depends(get_book_service),
    db : AsyncSession = Depends(get_session), 
    ):
        book = await book_service.get_book(db, book_id)
        return book
    
@book_router.post('/', response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(
        book_data : BookCreate,
        db : AsyncSession = Depends(get_session),
        book_service : BookService = Depends(get_book_service)       
    ):
        result = await book_service.create_book(db, book_data)
        return result

@book_router.patch('/{book_id}', response_model=Book , status_code=status.HTTP_200_OK)
async def update_book(
        book_id : str, 
        book_data :BookUpdate ,
        db : AsyncSession = Depends(get_session),
        book_service : BookService = Depends(get_book_service)       
    ):
        result = await book_service.update_book(db, book_id, book_data)
        return result

@book_router.delete('/{book_id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
        book_id : str, 
        db : AsyncSession = Depends(get_session),
        book_service : BookService = Depends(get_book_service)
    ):
        await book_service.delete_book(db, book_id)


        
        


