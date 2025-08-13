from sqlmodel import SQLModel, Field, Relationship
from uuid import uuid4, UUID
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects import postgresql as pg
from typing import  List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.book import Book



class User(SQLModel, table = True):
    id : UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    username :str =  Field(nullable=False, unique=True, index=True)
    email : str = Field(nullable=False, unique=True, index=True)
    first_name : str = Field(nullable=True)
    last_name : str = Field(nullable=True)
    is_verified : bool = Field(default=False)
    password_hash:str = Field(exclude=True)
    role : str = Field(sa_column= Column(pg.VARCHAR, server_default="user"))
    books :List["Book"] = Relationship(back_populates='user')
    
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
    updated_at : datetime = Field(
        default_factory = lambda:datetime.now(timezone.utc),  
        sa_column=Column(DateTime(timezone=True), nullable=False))
