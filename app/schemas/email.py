from pydantic import BaseModel

class EmailModel(BaseModel):
    emails : list[str]