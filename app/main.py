from fastapi import FastAPI
from api import book_routes


app = FastAPI(docs_url='/docs')
app.include_router(book_routes.router, prefix='api/vl')