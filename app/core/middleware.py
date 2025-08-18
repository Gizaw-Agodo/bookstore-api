from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import Response
import time
from typing import Callable, Awaitable
import logging

logger = logging.getLogger('uvicorn.access')
logger.disabled = True

def register_middleware(app: FastAPI) -> None:
    
    @app.middleware("http")
    async def custom_logging( # type: ignore
        request: Request, 
        call_next : Callable[[Request], Awaitable[Response]]
        ) -> Response:

        start_time = time.time()
        print('start time', start_time)

        response: Response = await call_next(request)
        duration = time.time() - start_time

        logger.info(
            f"{request.method} {request.url.path} "
            f"- {response.status_code} - {duration:.3f}s"
        )
       
        return response 
    