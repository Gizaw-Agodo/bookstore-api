from fastapi import APIRouter, Depends, status
from app.schemas.auth import UserCreate, UserLoginModel
from app.core.dependencies import get_auth_service, get_user_service, get_email_service
from app.services.auth_service import AuthService
from app.services.email_service import EmailService
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.database import get_session
from app.core.security import  create_token, verify_refresh_token, verify_access_token, decode_url_safe_token
from fastapi.responses import JSONResponse
from app.schemas.auth import RefreshTokenRequestModel, RevokeTokenRequestModel
from fastapi import HTTPException
from app.core.dependencies import get_current_user
from app.models.user import User
from app.core.redis import add_jti_to_token_blocklist
from app.core.security import role_checker
from app.schemas.auth import LoginResponse, UserInfo
from app.services.user_service import UserService
from app.schemas.email import EmailModel
from app.core.security import create_url_safe_token
from app.core.config import settings
from app.schemas.auth import ForgotPasswordModel, ResetPasswordModel

auth_router = APIRouter()

@auth_router.post('/signup', status_code=status.HTTP_201_CREATED)
async def create_user_account(
    user_data : UserCreate,  
    auth_service:AuthService =  Depends(get_auth_service), 
    db: AsyncSession  =  Depends(get_session), 
    email_service : EmailService = Depends(get_email_service)
):
    token = create_url_safe_token({"email": user_data.email})
    verification_link = f"http://{settings.domain}/verify?token={token}"

    new_user = await auth_service.create_user(db, user_data)

    await email_service.send_email(
        recipients= [new_user.email], 
        subject="Verify Your account",
        template_body = {
            "username" : new_user.username,
            "verification_link" : verification_link
            },
        template_name = "verify_email.html"
        )
    
    return new_user

@auth_router.post('verify/{token}')
async def verify_email_token(
    token : str,
    user_service : UserService = Depends(get_user_service), 
    db : AsyncSession  = Depends(get_session)
    ):
    response =  decode_url_safe_token(token)
    email = response.get('email')
    await user_service.verify_user(email, db)


@auth_router.post('/login', status_code=status.HTTP_200_OK)
async def user_login(
    login_data :UserLoginModel , 
    auth_service : AuthService = Depends(get_auth_service), 
    db : AsyncSession = Depends(get_session)
):
    result = await auth_service.login(db, login_data)
    
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

@auth_router.post('/send-verification-email')
async def send_verification_email(
    email_data :EmailModel,
    email_service:EmailService =  Depends(get_email_service),
    ):

    await email_service.send_email(
        recipients= email_data.emails, 
        subject="Verify Your account",
        template_body = {
            "username" : "Gizaw",
            "verification_link" : "http://localhost/verify"
            },
        template_name = "verify.html"
        )
    
    return {"Message" : "Email sent successfully"}



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



@auth_router.post('/forgot-password')
async def forgot_password(
   data : ForgotPasswordModel, 
   db : AsyncSession = Depends(get_session),
   user_service : UserService = Depends(get_user_service), 
   email_service : EmailService = Depends(get_email_service)
):
    user = await user_service.get_user_by_email(data.email, db)

    token = create_url_safe_token({"email": data.email})
    reset_link = f"http://{settings.domain}/api/v1/auth/reset-password?token={token}"

    await email_service.send_email(
        recipients= [data.email], 
        subject="Password Reset Request",
        template_name="reset_password.html",
        template_body={"username": user.username, "reset_link": reset_link}
        )
    
    return {"Message" : "Password reset email sent successfully"}


@auth_router.post('/reset-password/{token}')
async def reset_password(
    data : ResetPasswordModel, 
    token : str,
    auth_service :AuthService = Depends(get_auth_service),
    db : AsyncSession = Depends(get_session)
):
    response =  decode_url_safe_token(token)
    email = response.get('email')
    await auth_service.reset_password(email,data, db)
    return {"message":"password reseted successfuly"}

        