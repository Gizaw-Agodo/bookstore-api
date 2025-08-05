from fastapi import APIRouter, Depends, status
from app.schemas.auth import UserCreate, UserLoginModel
from app.core.dependencies import get_auth_service
from app.services.auth_service import AuthService
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.database import get_session
from app.core.security import verify_password, create_token, create_refresh_token, verify_refresh_token
from fastapi.responses import JSONResponse
from app.schemas.auth import RefreshTokenRequestModel
from fastapi import HTTPException


auth_router = APIRouter()

@auth_router.post('/signup', status_code=status.HTTP_201_CREATED)
async def create_user_account(
    user_data : UserCreate,  
    auth_service:AuthService =  Depends(get_auth_service), 
    db: AsyncSession  =  Depends(get_session)
):
    new_user = await auth_service.create_user(db, user_data)
    return new_user

@auth_router.post('/login', status_code=status.HTTP_200_OK)
async def user_login(
    login_data :UserLoginModel , 
    auth_service : AuthService = Depends(get_auth_service), 
    db : AsyncSession = Depends(get_session)
):
    user = await auth_service.get_user_by_email(db, login_data.email)
    if user is not None : 
        is_password_valid = verify_password(user.password_hash, login_data.password)
        if is_password_valid:
            access_token = create_token({"email" : user.email,"id" : str(user.id)})
            refresh_token = create_refresh_token({"email" : user.email,"id" : str(user.id)})
           
            return JSONResponse(
                content={
                    "message":"Login Successful", 
                    "access_token": access_token, 
                    "refresh_token": refresh_token, 
                    "user" : {
                        "email" : user.email, 
                        "id": str(user.id), 
                        "username": user.username
                    }
                }
            )

@auth_router.get('/refresh-token')
async def get_new_access_token(
    token_data : RefreshTokenRequestModel, 
    auth_service : AuthService = Depends(get_auth_service),
    db : AsyncSession = Depends(get_session)
    ):
    payload = verify_refresh_token(token_data.refresh_token)
    if not payload :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    
    email = payload["email"]
    user = await auth_service.get_user_by_email(db, email)
    if not user : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    
    access_token = create_token({"email" : user.email,"id" : str(user.id)})
    return JSONResponse( content= {  "access_token": access_token } )
    






        