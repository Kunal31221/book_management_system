# app/schemas.py
from pydantic import BaseModel
from typing import List, Optional


class BookBase(BaseModel):
    title: str
    author: str
    genre: str
    year_published: int
    summary: Optional[str] = None


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    pass


class Book(BookBase):
    id: int

    class Config:
        orm_mode = True


class ReviewBase(BaseModel):
    book_id: int
    user_id: int
    review_text: str
    rating: float


class ReviewCreate(ReviewBase):
    pass


class Review(ReviewBase):
    id: int

    class Config:
        orm_mode = True
