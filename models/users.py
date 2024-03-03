from database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, index=True, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    items = relationship('Books', back_populates='author')
