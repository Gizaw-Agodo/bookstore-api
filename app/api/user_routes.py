from fastapi import APIRouter, Depends
from app.core.security import role_checker
from app.services.user_service import UserService
from app.core.dependencies import get_user_service, get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from app.models.book import Book

user_router = APIRouter()

@user_router.get('/{user_id}/books', response_model=List[Book])
async def get_user_books(
        user_id : str, 
        _:bool =  Depends(role_checker(["user" , "admin"])), 
        user_service :UserService = Depends(get_user_service), 
        db : AsyncSession = Depends(get_session)
        ):
    books = await user_service.get_user_books(user_id, db)
    return books
