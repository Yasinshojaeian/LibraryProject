from typing import List

from fastapi import APIRouter, Depends

from auth import oauth2
from db_crud import categories
from dependencies import get_db
from schemas.category import CategoriesBase, CategoryDisplay
from schemas.users import UserBase

router = APIRouter(prefix='/category')


# create category
@router.post('/create/', response_model=CategoryDisplay)
def create_category(category: CategoriesBase, db=Depends(get_db),
                    current_user: UserBase = Depends(oauth2.get_current_user)):
    return categories.create_category(db, category)




# read All categories

@router.get('/all/', response_model=List[CategoryDisplay])
def read_all_categories(db=Depends(get_db), current_user: UserBase = Depends(oauth2.get_current_user)):
    result = categories.get_all_categories(db)
    for i in result:
        i.books
    return result


# read category

@router.get('/{pk}/')
def get_category(pk: int, db=Depends(get_db), current_user: UserBase = Depends(oauth2.get_current_user)):
    data = categories.get_category(pk, db)
    books = data.books
    return {
        "data": data,
    }


# update category

@router.post('/update/{pk}/')
def update_category(pk: int, user: CategoriesBase, db=Depends(get_db),
                    current_user: UserBase = Depends(oauth2.get_current_user)):
    return categories.update_category(pk, db, user)


# delete category

@router.get('/delete/{pk}/')
def delete_category(pk: int, db=Depends(get_db), current_user: UserBase = Depends(oauth2.get_current_user)):
    return categories.delete_category(pk, db)


# Assign Book To Categorise

@router.post("/assign/category/{category_id}/books/{book_id}")
def assign_book(category_id: int, book_id: int, db=Depends(get_db)):
    return categories.assign_book(category_id, book_id, db)

# Remove Book To Categorise
@router.delete("/remove/category/{category_id}/books/{book_id}")
def remove_book(category_id: int, book_id: int, db=Depends(get_db)):
    return categories.remove_book(category_id, book_id, db)