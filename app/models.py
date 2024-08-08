# # from sqlalchemy import Column, Integer, String, ForeignKey, Float
# # from sqlalchemy.orm import relationship
# # from app.database import Base
# #
# #
# # class Book(Base):
# #     __tablename__ = 'books'
# #     id = Column(Integer, primary_key=True, index=True)
# #     title = Column(String, index=True)
# #     author = Column(String, index=True)
# #     genre = Column(String, index=True)
# #     year_published = Column(Integer)
# #     summary = Column(String)
# #
# #
# # class Review(Base):
# #     __tablename__ = 'reviews'
# #     id = Column(Integer, primary_key=True, index=True)
# #     book_id = Column(Integer, ForeignKey('book.id'))
# #     user_id = Column(Integer)
# #     review_text = Column(String)
# #     rating = Column(Float)
# #
# #     book = relationship("Book", back_populates='reviews')
# #
# #
# # Book.reviews = relationship('Review', order_by=Review.id, back_populates="book")
#
# # models.py
#
# from sqlalchemy import Column, Integer, String, ForeignKey
# from sqlalchemy.orm import relationship
# from app.database import Base
#
#
# class Book(Base):
#     __tablename__ = 'books'
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String(100), index=True)
#     author = Column(String(100), index=True)
#     genre = Column(String(100), index=True)
#     year_published = Column(Integer)
#     reviews = relationship("Review", back_populates="book")
#
#
# class Review(Base):
#     __tablename__ = 'reviews'
#     id = Column(Integer, primary_key=True, index=True)
#     content = Column(String(100), index=True)
#     book_id = Column(Integer, ForeignKey('books.id'))
#     book = relationship("Book", back_populates="reviews")

from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database import Base


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    author = Column(String(100), index=True)
    genre = Column(String(100), index=True)
    year_published = Column(Integer)
    summary = Column(String, nullable=True)
    reviews = relationship("Review", back_populates="book")


class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    user_id = Column(Integer)
    review_text = Column(String)
    rating = Column(Float)
    book = relationship("Book", back_populates="reviews")

