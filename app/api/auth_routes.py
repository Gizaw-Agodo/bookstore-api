from fastapi import APIRouter, Depends, status
from app.schemas.auth import UserCreate, UserLoginModel
from app.core.dependencies import get_auth_service, get_user_service
from app.services.auth_service import AuthService
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.database import get_session
from app.core.security import  create_token, verify_refresh_token, verify_access_token
from fastapi.responses import JSONResponse
from app.schemas.auth import RefreshTokenRequestModel, RevokeTokenRequestModel
from fastapi import HTTPException
from app.core.dependencies import get_current_user
from app.models.user import User
from app.core.redis import add_jti_to_token_blocklist
from app.core.security import role_checker
from app.schemas.auth import LoginResponse, UserInfo
from app.services.user_service import UserService

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
    result = await auth_service.login(db, login_data)
    if not result:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
    
    return LoginResponse(
         message= "Login successfull",
         access_token=result['access_token'], 
         refresh_token=result['refresh_token'],
         user=UserInfo(
                email=result["user"].email,
                id=str(result["user"].id),
                username=result["user"].username,
            )
      )


@auth_router.get('/me')
async def get_user(curr_user : User = Depends(get_current_user),  _:bool = Depends(role_checker(['admin', 'user']))):
    return curr_user


@auth_router.get('/refresh-token')
async def get_new_access_token(
    token_data : RefreshTokenRequestModel, 
    user_service : UserService = Depends(get_user_service),
    db : AsyncSession = Depends(get_session)
    ):
    payload = verify_refresh_token(token_data.refresh_token)
    if not payload :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    
    email = payload["email"]
    user = await user_service.get_user_by_email(email, db)
    if not user : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    
    access_token = create_token({"email" : user.email,"id" : str(user.id)})
    return JSONResponse( content= {  "access_token": access_token } )


    
@auth_router.post('/logout')
async def revoke_token( 
    token_data :RevokeTokenRequestModel, 
    _: User = Depends(get_current_user),
    ):
    
    access_token = token_data.access_token
    payload = verify_access_token(access_token)

    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    jti = payload['jti']
    await add_jti_to_token_blocklist(jti)

    return JSONResponse(content={"message" : "Logout successfull"}, status_code=status.HTTP_200_OK)






        