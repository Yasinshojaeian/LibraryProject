from pydantic import BaseModel
from typing import List


# User in Book Display
class User(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


class Category(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True


class BooksBase(BaseModel):
    title: str
    description: str
    published: bool
    published_date: str
    page: int
    author_id: List[int] | None = None
    category_id: List[int] | None = None


class BookDisplay(BaseModel):
    id: int
    title: str
    description: str
    published: bool
    author: List[User] | None = None
    categories: List[Category] | None = None

    class Config:
        orm_mode = True

