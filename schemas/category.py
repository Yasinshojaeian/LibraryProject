from pydantic import BaseModel
from typing import List


class CategoriesBase(BaseModel):
    title: str


class CategoryDisplay(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True
