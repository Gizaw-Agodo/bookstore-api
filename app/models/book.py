from datetime import date
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4

class Book(SQLModel , table = True) : 
    id : UUID = Field(default_factory= uuid4, primary_key=True, index=True )
    title : str 
    author : str 
    publisher : str 
    page_count : int 
    language : str 
    created_at : date 
    updated_at : date
