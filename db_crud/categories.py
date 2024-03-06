from sqlalchemy.orm.session import Session
from schemas.category import *
from models.books import Category, Books
from fastapi.exceptions import HTTPException
from fastapi import status


def create_category(db: Session, request: CategoriesBase):
    category = Category(
        title=request.title,
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def assign_book(category_id: int, book_id: int, db: Session):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail=f"Category whith {category_id} not found")

    book = db.query(Books).filter(Books.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if book in category.books:
        raise HTTPException(status_code=404, detail="Book is already assigned to this category")

    category.books.append(book)
    db.commit()
    return {"message": "Book assigned successfully"}


def remove_book(category_id: int, book_id: int, db: Session):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    book = db.query(Books).filter(Books.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if book not in category.books:
        raise HTTPException(status_code=404, detail="Book is not assigned to this category")

    category.books.remove(book)
    db.commit()
    return {"message": "book removed successfully"}


def update_category(pk, db: Session, request: CategoriesBase):
    category = db.query(Category).filter(Category.id == pk)
    check = category.first()
    if not check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Category with {pk} not found')
    category.update({
        Category.title: request.title,
    })
    db.commit()
    return 'Updated !'


def get_all_categories(db: Session):
    return db.query(Category).all()


def get_category(pk, db: Session):
    category = db.query(Category).filter(Category.id == pk).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"category with id {pk} not found!")
    return category


def delete_category(pk, db: Session):
    category = get_category(pk, db)
    db.delete(category)
    db.commit()
    return 'ok'
