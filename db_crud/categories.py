from sqlalchemy.orm.session import Session
from schemas.category import *
from models.books import Category
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
    article = db.query(Category).filter(Category.id == pk).first()
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"article with id {pk} not found!")
    return article


def delete_category(pk, db: Session):
    category = get_category(pk, db)
    db.delete(category)
    db.commit()
    return 'ok'
