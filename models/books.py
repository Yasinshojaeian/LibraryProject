from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship

category_books = Table(
    "category_books",
    Base.metadata,
    Column("books_id", Integer, ForeignKey("books.id")),
    Column("categories_id", Integer, ForeignKey("categories.id"))
)


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, index=True, primary_key=True)
    title = Column(String)

    # book_id = Column(Integer, ForeignKey('users.id'))
    # books = relationship('Books', back_populates='category')
    books = relationship("Books", secondary=category_books, back_populates="categories")


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
    #
    # category_id = Column(Integer, ForeignKey('categories.id'))
    # category = relationship('Category', back_populates='books')
    categories = relationship("Category", secondary=category_books, back_populates="books")
