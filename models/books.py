from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, index=True, primary_key=True)
    title = Column(String)

    book_id = Column(Integer, ForeignKey('users.id'))
    books = relationship('Books', back_populates='category')


class Books(Base):
    __tablename__ = 'books'

    id = Column(Integer, index=True, primary_key=True)
    title = Column(String)
    description = Column(String)
    published = Column(Boolean)
    published_date = Column(String)
    page = Column(Integer)

    author_id = Column(Integer, ForeignKey('users.id'))
    author = relationship('User', back_populates='items')

    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category', back_populates='books')
