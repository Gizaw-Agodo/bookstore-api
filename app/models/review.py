from sqlmodel import SQLModel, Field, Column, Relationship
from uuid import UUID, uuid4
from typing import Optional, TYPE_CHECKING
from datetime import datetime, timezone
from sqlalchemy import DateTime

if TYPE_CHECKING: 
    from app.models.user import User
    from app.models.book import Book

class Review(SQLModel, table = True):
    id : UUID = Field(default_factory=uuid4, primary_key = True, index= True)
    rating : int = Field(lt= 5, default=0)
    review_text : str

    user_id : Optional[UUID] = Field(foreign_key='user.id', default=None)
    book_id : Optional[UUID] = Field(foreign_key="book.id", default=None)
    user : Optional["User"] = Relationship(back_populates='reviews')
    book : Optional["Book"] = Relationship(back_populates="reviews")

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
    updated_at : datetime = Field(
        default_factory = lambda:datetime.now(timezone.utc),  
        sa_column=Column(DateTime(timezone=True), nullable=False))