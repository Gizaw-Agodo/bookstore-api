from sqlmodel import SQLModel, Field, Relationship, Column
from uuid import UUID, uuid4
from typing import Optional, TYPE_CHECKING, List
from datetime import datetime, timezone
from sqlalchemy import DateTime

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.review import Review

class Book(SQLModel , table = True) : 
    id : UUID = Field(default_factory= uuid4, primary_key=True, index=True )
    title : str 
    author : str 
    publisher : str 
    page_count : int 
    language : str 

    user_id : Optional[UUID] = Field(foreign_key="user.id", default=None)
    user : Optional["User"] = Relationship(back_populates='books')
    reviews : List['Review'] = Relationship(back_populates="book")
    
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
    updated_at : datetime = Field(
        default_factory = lambda:datetime.now(timezone.utc),  
        sa_column=Column(DateTime(timezone=True), nullable=False))
