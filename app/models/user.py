from sqlmodel import SQLModel, Field
from uuid import uuid4, UUID
from datetime import datetime, timezone

class User(SQLModel, table = True):
    id : UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    username :str =  Field(nullable=False, unique=True, index=True)
    email : str = Field(nullable=False, unique=True, index=True)
    first_name : str = Field(nullable=True)
    last_name : str = Field(nullable=True)
    is_verified : bool = Field(default=False)
    created_at : datetime = Field(default_factory = lambda:datetime.now(timezone.utc), nullable=False)
    updated_at : datetime = Field(default_factory = lambda:datetime.now(timezone.utc), nullable=False)
