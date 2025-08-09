from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username:str = Field(max_length=8)
    email : str = Field(max_length=8)
    password : str = Field(min_length=6)
    first_name : str
    last_name:str

class UserLoginModel(BaseModel):
    email : str
    password : str

class RefreshTokenRequestModel(BaseModel):
    refresh_token : str

class RevokeTokenRequestModel(BaseModel):
    access_token : str