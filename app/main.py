from fastapi import FastAPI
from app.api.book_routes import book_router
from app.api.auth_routes import auth_router
# from app.core.database import create_db
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app : FastAPI):
    print('server is starting...')
    # await create_db()
    try:
        pass
    except:
        pass

    yield 

    print('server has been stoped.')




version = "v1"
app = FastAPI(
    version=version,
    docs_url='/docs',
    title="Bookly api", 
    description=" a rest api for book review web service", 
    lifespan= lifespan
)



# add routes
app.include_router(book_router, prefix=f'/api/{version}/books', tags=['Books'])
app.include_router(auth_router, prefix=f'/api/{version}/auth', tags=['Auth'])