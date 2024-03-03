from fastapi import APIRouter, Depends, HTTPException
from models.users import *
from dependencies import get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from fastapi import status
from db_crud.hash import Hash
from auth import oauth2

router = APIRouter(tags=['authentications'])


@router.post("/token")
def get_token(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(request.username == User.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid credential")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid password")

    access_token = oauth2.create_access_token(data={'sub': request.username})

    return {
        'access_token': access_token,
        'type_token': "bearer",
        'userID': user.id,
        'username': user.username

    }
