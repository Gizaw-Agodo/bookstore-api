from redis.asyncio import Redis
from app.core.config import settings

token_blocklist = Redis( host = settings.REDIS_HOST,  port= settings.REDIS_PORT, db=0)
JTI_EXPIRY_SECONDS = 3600

async def add_jti_to_token_blocklist(jti : str) -> None:
    await token_blocklist.set(name = jti, value= True, ex = JTI_EXPIRY_SECONDS)

async def token_in_blocklist(jti:str ) -> bool:
    return False
    # existing_jti = await token_blocklist.get(jti)
    # return existing_jti is not None