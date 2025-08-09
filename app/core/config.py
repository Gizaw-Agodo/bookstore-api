from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings): 
    app_name : str = "test app"
    DATABASE_URL: str = ""
    
    #tokens 
    ACCESS_SECRET_KEY : str = ""
    REFRESH_SECRET_KEY : str = ""
    ALGORITHM:str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES:int = 30
    REFRESH_TOKEN_EXPIRE_DAYS:int = 7

    REDIS_HOST : str = 'localhost'
    REDIS_PORT :int = 6379


    model_config = SettingsConfigDict(env_file='.env', extra='ignore')
    
settings = Settings()
