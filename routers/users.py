from typing import List

from fastapi import APIRouter, Depends

from auth import oauth2
from db_crud import users
from dependencies import get_db
from schemas.users import UserBase, UserDisplay

router = APIRouter(prefix='/user')


# create user
@router.post('/create/', response_model=UserDisplay)
def create_user(user: UserBase, db=Depends(get_db)):
    return users.create_user(db, user)


# read All user

@router.get('/all/',response_model=List[UserDisplay])
def read_all_user(db=Depends(get_db), token: UserBase = Depends(oauth2.get_current_user)):
    query = users.get_all_users(db)
    for i in query:
        books = i.items
    return query


# read user

@router.get('/{pk}/', response_model=UserDisplay)
def read_user(pk: int, db=Depends(get_db), token: UserBase = Depends(oauth2.get_current_user)):
    return users.get_user(pk, db)


# update user

@router.post('/update/{pk}/')
def update_user(pk: int, user: UserBase, db=Depends(get_db), token: UserBase = Depends(oauth2.get_current_user)):
    return users.update_user(pk, db, user)


# delete user

@router.get('/delete/{pk}/')
def delete_user(pk: int, db=Depends(get_db), token: UserBase = Depends(oauth2.get_current_user)):
    return users.delete_user(pk, db)
