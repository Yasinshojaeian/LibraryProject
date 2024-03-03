from sqlalchemy.orm.session import Session
from schemas.users import UserBase
from models.users import User
from .hash import Hash
from fastapi.exceptions import HTTPException
from fastapi import status
from exceptions import EmailNotValid


def create_user(db: Session, request: UserBase):
    if "@" not in request.email:
        raise EmailNotValid("Email Not Valid ! ")

    user = User(
        username=request.username,
        email=request.email,
        password=Hash.bcrypt(request.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(pk, db: Session, request: UserBase):
    user = db.query(User).filter(User.id == pk)
    user.update({
        User.username: request.username,
        User.email: request.email,
        User.password: Hash.bcrypt(request.password)
    })
    db.commit()
    return 'ok'


def get_all_users(db: Session):
    return db.query(User).all()


def get_user(pk, db: Session):
    user = db.query(User).filter(User.id == pk).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {pk} not found!")
    return user


def get_user_by_username(username, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {username} not found!")
    return user

def delete_user(pk, db: Session):
    user = get_user(pk, db)
    db.delete(user)
    db.commit()
    return 'ok'
