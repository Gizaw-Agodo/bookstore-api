from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.review import ReviewCreateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.dependencies import get_review_service, get_current_user
from app.core.database import get_session
from app.services.review_service import ReviewService
from app.models.user import User
from uuid import UUID
 


review_router = APIRouter(prefix='')

@review_router.post('/book/{book_id}')
async def add_review_to_book(
    book_id : UUID, 
    review_data : ReviewCreateModel, 
    db : AsyncSession =  Depends(get_session), 
    current_user : User = Depends(get_current_user),
    review_service : ReviewService = Depends(get_review_service)
):
    try:
        new_review = await review_service.add_review_to_book(db, review_data, book_id,current_user.id)
        return new_review
    except:
        HTTPException(status_code = status.HTTP_400_BAD_REQUEST ,detail='not able to create')