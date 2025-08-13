from datetime import date
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User

class Book(SQLModel , table = True) : 
    id : UUID = Field(default_factory= uuid4, primary_key=True, index=True )
    title : str 
    author : str 
    publisher : str 
    page_count : int 
    language : str 
    created_at : date 
    updated_at : date
    user_id : Optional[UUID] = Field(foreign_key="user.id", default=None)
    user : Optional["User"] = Relationship(back_populates='books')
