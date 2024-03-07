from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship

category_books = Table(
    "category_books",
    Base.metadata,
    Column("books_id", Integer, ForeignKey("books.id")),
    Column("categories_id", Integer, ForeignKey("categories.id"))
)

author_books = Table(
    "author_books",
    Base.metadata,
    Column("books_id", Integer, ForeignKey("books.id")),
    Column("author_id", Integer, ForeignKey("users.id"))
)


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, index=True, primary_key=True)
    title = Column(String)

    books = relationship("Books", secondary=category_books, back_populates="categories")


class Books(Base):
    __tablename__ = 'books'

    id = Column(Integer, index=True, primary_key=True)
    title = Column(String)
    description = Column(String)
    published = Column(Boolean)
    published_date = Column(String)
    page = Column(Integer)

    author = relationship('User', secondary=author_books, back_populates='items')
    categories = relationship("Category", secondary=category_books, back_populates="books")
