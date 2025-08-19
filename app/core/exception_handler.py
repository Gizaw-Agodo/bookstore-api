from fastapi import Request, FastAPI
from app.core.errors import CoreError
from fastapi.responses import JSONResponse
from app.core.errors import CoreError
from typing import Callable, cast
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

exception_handler = Callable[[Request, Exception], JSONResponse]

async def core_exception_handler(req : Request, exc : CoreError) -> JSONResponse:
    return JSONResponse(
        status_code = exc.status_code,
        content= {
            "status": exc.status_code,
            "title": exc.__class__.__name__,
            "detail": str(exc.detail),
        }, 
        headers= exc.headers
    )

async def validate_exception_handler(req:Request, exc : RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code =422,
        content= {
            "status": 422,
            "title": exc.__class__.__name__,
            "detail": str(exc.errors()),
        }, 
    )

def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(CoreError, cast(exception_handler,core_exception_handler ) )
    app.add_exception_handler(RequestValidationError,cast(exception_handler,validate_exception_handler )  )
