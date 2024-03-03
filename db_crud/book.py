from sqlalchemy.orm.session import Session
from schemas.books import *
from models.books import Books
from fastapi.exceptions import HTTPException
from fastapi import status
import models

def create_book(db: Session, request: BooksBase):
    book = Books(
        title=request.title,
        description=request.description,
        published=request.published,
        page=request.page,
        published_date=request.published_date,
        author_id=request.author_id,
        category_id=request.category_id,
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def update_book(pk, db: Session, request: BooksBase):
    book = db.query(Books).filter(Books.id == pk)
    book.update({
        Books.title: request.title,
        Books.description: request.description,
        Books.published: request.published,
        Books.published_date: request.published_date,
        Books.author_id: request.author_id,
        Books.category_id: request.category_id,

    })
    db.commit()
    return 'ok'


def get_all_book(db: Session):
    return db.query(Books).all()


def get_book(pk, db: Session):
    book = db.query(Books).filter(Books.id == pk).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"article with id {pk} not found!")
    return book


def delete_book(pk, db: Session):
    book = get_book(pk, db)
    db.delete(book)
    db.commit()
    return 'ok'


def search_book(db: Session, q):
    books = db.query(Books).filter(Books.title == q)
    return books


def get_book_with_category(db: Session, cat: str):
    category = db.query(models.books.Category).filter(models.books.Category.title == cat).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Category Not Found !')
    books = db.query(Books).filter(Books.category_id == category.id)
    return books
