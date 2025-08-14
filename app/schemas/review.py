
from pydantic import BaseModel

class ReviewCreateModel(BaseModel):
    review_text : str
    rating : int

