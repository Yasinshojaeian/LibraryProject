from typing import List

from fastapi import APIRouter, Depends

from auth import oauth2
from db_crud import book
from dependencies import get_db
from schemas.books import BooksBase, BookDisplay
from schemas.users import UserBase

router = APIRouter(prefix='/book')


# create book
@router.post('/create/', response_model=BookDisplay)
def create_book(article: BooksBase, db=Depends(get_db)):
    return book.create_book(db, article)


# read All book

@router.get('/all/', response_model=List[BookDisplay])
def read_all_books(db=Depends(get_db)):
    return book.get_all_book(db)


@router.get('/search/', response_model=List[BookDisplay])
def search_books(db=Depends(get_db), q: str | None = None):
    return book.search_book(db, q)


@router.get('/category/{cat}', response_model=List[BookDisplay])
def search_books(db=Depends(get_db), cat: str | None = None):
    return book.get_book_with_category(db, cat)


# read book

@router.get('/{pk}/')
def read_book(pk: int, db=Depends(get_db), current_user: UserBase = Depends(oauth2.get_current_user)):
    return {
        "data": book.get_book(pk, db),
        "current_user": current_user
    }


# update book

@router.post('/update/{pk}/')
def update_book(pk: int, user: BooksBase, db=Depends(get_db)):
    return book.update_book(pk, db, user)


# delete book

@router.get('/delete/{pk}/')
def delete_book(pk: int, db=Depends(get_db)):
    return book.delete_book(pk, db)
