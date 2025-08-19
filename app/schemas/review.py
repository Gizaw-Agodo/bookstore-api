
from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime

class ReviewCreateModel(BaseModel):
    review_text : str
    rating : int


class ReviewModel(BaseModel):
    id : UUID
    rating : int
    review_text : str
    user_id : Optional[UUID] 
    book_id : Optional[UUID]
    created_at: datetime
    updated_at : datetime