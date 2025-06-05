from pydantic import BaseModel

class BookModel(BaseModel):
    book_title: str
    author: str
    year_of_publication: str