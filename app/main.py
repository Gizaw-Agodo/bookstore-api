from fastapi import FastAPI
from app.api.book_routes import book_router
from app.api.auth_routes import auth_router
from app.api.user_routes import user_router
from app.api.review_routes import review_router
from app.core.exception_handler import register_exception_handlers
from app.core.middleware import register_middleware

from fastapi.openapi.utils import get_openapi

from contextlib import asynccontextmanager

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="My API",
        version="1.0.0",
        description="JWT-based Auth API",
        routes=app.routes,
    )

    # 👇 Replace OAuth2 with simple Bearer auth
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

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
app.openapi = custom_openapi
register_exception_handlers(app)
register_middleware(app)



# add routes
app.include_router(book_router, prefix=f'/api/{version}/books', tags=['Books'])
app.include_router(auth_router, prefix=f'/api/{version}/auth', tags=['Auth'])
app.include_router(user_router,prefix=f'/api/{version}/users' , tags=["Users"])
app.include_router(review_router, prefix= f'/api/{version}/reviews', tags=["Review"])