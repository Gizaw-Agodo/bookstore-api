from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username:str = Field(max_length=8)
    email : str = Field(max_length=64)
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

class UserInfo(BaseModel):
    email: str
    id: str
    username: str

class LoginResponse(BaseModel):
    message: str
    access_token: str
    refresh_token: str
    user: UserInfo

class ForgotPasswordModel(BaseModel):
    email: str

class ResetPasswordModel(BaseModel):
    new_password : str
    confirm_password : str