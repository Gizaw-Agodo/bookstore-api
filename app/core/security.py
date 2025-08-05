from passlib.context import CryptContext
from datetime import timedelta, datetime, timezone
from jose import  jwt, JWSError
from app.core.config import settings
import uuid

context = CryptContext(schemes=['bcrypt'])

def hash_password(password : str):
    return context.hash(password)

def verify_password(hash:str, password : str):
    return context.verify(password, hash)

def create_token(user_data : dict[str, str| datetime |bool ]):
    to_encode = user_data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "jti": str(uuid.uuid4())})
    return jwt.encode(claims = to_encode, key = settings.ACCESS_SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(user_data : dict[str, str| datetime |bool ]):
    to_encode = user_data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "jti": str(uuid.uuid4())})
    return jwt.encode(claims = to_encode, key = settings.REFRESH_SECRET_KEY, algorithm=settings.ALGORITHM)

def verify_access_token(token : str):
    try:
        payload = jwt.decode(token, key = settings.ACCESS_SECRET_KEY, algorithms=settings.ALGORITHM)
        return payload
    except JWSError : 
        return None

def verify_refresh_token(refresh_token : str):
    try:
        payload = jwt.decode(refresh_token, key = settings.REFRESH_SECRET_KEY, algorithms=settings.ALGORITHM)
        return payload
    except JWSError : 
        return None

        
