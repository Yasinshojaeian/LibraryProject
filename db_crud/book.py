from sqlalchemy.orm.session import Session
from schemas.books import *
from models.books import Books , category_books
from fastapi.exceptions import HTTPException
from fastapi import status
import models
from models import users
from db_crud.categories import assign_book


def create_book(db: Session, request: BooksBase):
    book = Books(
        title=request.title,
        description=request.description,
        published=request.published,
        page=request.page,
        published_date=request.published_date
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def assign_author_book(author_id: int, book_id: int, db: Session):
    user = db.query(users.User).filter(users.User.id == author_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with {author_id} not found")
    book = db.query(Books).filter(Books.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if len(user.items) >= 2:
        raise HTTPException(status_code=400,
                            detail="This author is currently the author of two books. An author cannot be the author of more than two books")

    if book in user.items:
        raise HTTPException(status_code=404, detail="Book is already assigned to this user")
    user.items.append(book)
    db.commit()
    return {"message": "Book assigned successfully"}


def remove_author_book(author_id: int, book_id: int, db: Session):
    user = db.query(users.User).filter(users.User.id == author_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    book = db.query(Books).filter(Books.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if book not in user.items:
        raise HTTPException(status_code=404, detail="Book is not assigned to this category")

    user.items.remove(book)
    db.commit()
    return {"message": "book removed successfully"}


def update_book(pk, db: Session, request: BooksBase):
    book = db.query(Books).filter(Books.id == pk)
    book.update({
        Books.title: request.title,
        Books.description: request.description,
        Books.published: request.published,
        Books.published_date: request.published_date,
    })
    if request.author_id:
        book = db.query(Books).filter(Books.id == pk).first()
        for user_id in request.author_id:
            assign_author_book(author_id=user_id, book_id=book.id, db=db)
    if request.category_id:
        book = db.query(Books).filter(Books.id == pk).first()
        for cat_id in request.category_id:
            assign_book(category_id=cat_id, book_id=book.id, db=db)
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category Not Found !')
    books = category.books
    return books
