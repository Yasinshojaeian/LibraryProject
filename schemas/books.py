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
    author_id: int
    category_id: int


class BookDisplay(BaseModel):
    title: str
    description: str
    published: bool
    author: User
    category: Category | None = None

    class Config:
        orm_mode = True
