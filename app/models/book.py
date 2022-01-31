from odmantic import Model
from typing import Optional


class BookModel(Model):
    keyword: Optional[str]
    publisher: Optional[str]
    price: Optional[int]
    image: Optional[str]

    class Config:
        collection = "books"
