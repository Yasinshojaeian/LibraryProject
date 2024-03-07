from pydantic import BaseModel
from typing import List


class User(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


class BookDisplay(BaseModel):
    title: str
    description: str
    published: bool
    author: List[User]

    # category: Category | None = None

    class Config:
        orm_mode = True


class CategoriesBase(BaseModel):
    title: str


class CategoryDisplay(BaseModel):
    id: int
    title: str
    books: List[BookDisplay]

    class Config:
        orm_mode = True
