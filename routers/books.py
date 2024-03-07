from typing import List

from fastapi import APIRouter, Depends

from auth import oauth2
from db_crud import book
from dependencies import get_db
from schemas.books import BooksBase, BookDisplay
from schemas.users import UserBase
from db_crud import categories

router = APIRouter(prefix='/book')


# create book
@router.post('/create/')
def create_book(data: BooksBase, db=Depends(get_db)):
    new_book = book.create_book(db, data)
    if not data.category_id:
        return new_book
    for cat_id in data.category_id:
        categories.assign_book(category_id=cat_id, book_id=new_book.id, db=db)
    for user_id in data.author_id:
        book.assign_author_book(author_id=user_id, book_id=new_book.id, db=db)
    autors = new_book.author
    return {
        "message": "Book created successfully",
        "data": new_book
    }


@router.post("/assign/author/{author_id}/book/{book_id}")
def assign_author_book(author_id: int, book_id: int, db=Depends(get_db)):
    return book.assign_author_book(author_id, book_id, db)


@router.delete("/remove/author/{author_id}/book/{book_id}")
def remove_author_book(author_id: int, book_id: int, db=Depends(get_db)):
    return book.remove_author_book(author_id, book_id, db)


# read All book

@router.get('/all/', response_model=List[BookDisplay])
def read_all_books(db=Depends(get_db)):
    books = book.get_all_book(db)
    for i in books:
        i.author
        i.categories
    return books


@router.get('/search/', response_model=List[BookDisplay])
def search_books(db=Depends(get_db), q: str | None = None):
    return book.search_book(db, q)


@router.get('/category/{cat}', response_model=List[BookDisplay])
def get_books_with_category(db=Depends(get_db), cat: str | None = None):
    return book.get_book_with_category(db, cat)


# read book

@router.get('/{pk}/', response_model=BookDisplay)
def read_book(pk: int, db=Depends(get_db), current_user: UserBase = Depends(oauth2.get_current_user)):
    result = book.get_book(pk, db)

    return result


# update book

@router.post('/update/{pk}/')
def update_book(pk: int, data: BooksBase, db=Depends(get_db),
                current_user: UserBase = Depends(oauth2.get_current_user)):
    return book.update_book(pk, db, data)


# delete book

@router.get('/delete/{pk}/')
def delete_book(pk: int, db=Depends(get_db)):
    return book.delete_book(pk, db)
