from app.services.book_service import BookService

def get_book_service() -> BookService:
    return BookService()
