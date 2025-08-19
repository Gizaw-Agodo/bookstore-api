from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings): 
    app_name : str = "test app"
    DATABASE_URL: str = ""
    domain : str = "localhost:8000"
    
    #tokens 
    ACCESS_SECRET_KEY : str = ""
    REFRESH_SECRET_KEY : str = ""
    ALGORITHM:str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES:int = 30
    REFRESH_TOKEN_EXPIRE_DAYS:int = 7

    REDIS_HOST : str = 'localhost'
    REDIS_PORT :int = 6379

    #email config 
    MAIL_USERNAME: str = ''
    MAIL_PASSWORD: SecretStr = SecretStr('')
    MAIL_FROM: str = ''
    MAIL_PORT: int = 587
    MAIL_SERVER: str = 'smtp.gmail.com'
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = True


    model_config = SettingsConfigDict(env_file='.env', extra='ignore')
    
settings = Settings()
