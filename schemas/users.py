from pydantic import BaseModel
from typing import List


# category book in user display
class Category(BaseModel):
    title: str

    class Config:
        orm_mode = True


# book in user display
class Book(BaseModel):
    title: str
    description: str
    categories: List[Category]

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    password: str
    email: str


class UserDisplay(BaseModel):
    id: int
    username: str
    email: str
    items: List[Book]

    class Config:
        orm_mode = True
