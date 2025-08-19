from pydantic import BaseModel, Field
from datetime import date
from uuid import UUID
from typing import Optional, List
from datetime import datetime
from app.schemas.review import ReviewModel

class BookModel(BaseModel) : 
    id : UUID 
    title : str 
    author : str 
    publisher : str 
    page_count : int 
    language : str 

    user_id : Optional[UUID] 
    created_at: datetime 
    updated_at : datetime

class BooksResponse(BaseModel) : 
    id : int = Field(...,gt= 0, description="book id must be greater than 0")
    title : str = Field(..., min_length= 5 , max_length=100, description="title must be between 5 and 100")
    author : str = Field(..., min_length= 3, max_length= 50 , description= "Author name must be between 3 and 50")
    publisher : str = Field(..., min_length=3, max_length=50, description="Publisher name must be between 3 and 50")
    published_date : date = Field(..., description="Published date must be in format (yyyy-mm-dd)")
    page_count : int = Field(..., gt = 0 , le=5000, description="Page count must be between 0 and 500")
    language : str 

class BookCreate(BaseModel) : 
    title : str 
    author : str
    publisher : str 
    published_date : date
    page_count : int 
    language : str 
    created_at : date 
    updated_at : date


class BookUpdate(BaseModel) : 
    title : str = Field(..., min_length= 5 , max_length=100, description="title must be between 5 and 100")
    author : str = Field(..., min_length= 3, max_length= 50 , description= "Author name must be between 3 and 50")
    publisher : str = Field(..., min_length=3, max_length=50, description="Publisher name must be between 3 and 50")
    published_date : date = Field(..., description="Published date must be in format (yyyy-mm-dd)")
    page_count : int = Field(..., gt = 0 , le=5000, description="Page count must be between 0 and 500")
    language : str 

class BookDetailModel(BookModel):
    reviews : List[ReviewModel]

