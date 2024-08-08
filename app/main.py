from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db, engine, Base
from app.models import Book as BookModel, Review as ReviewModel
from app.schemas import Book, BookCreate, BookUpdate, Review, ReviewCreate
from app.crud import create_book, get_books, get_book, update_book, delete_book, create_review, get_reviews, get_summary, get_recommendations

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.post("/books", response_model=Book)
async def create_book_endpoint(book: BookCreate, db: AsyncSession = Depends(get_db)):
    return await create_book(db, book)


@app.get("/books", response_model=List[Book])
async def get_books_endpoint(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await get_books(db, skip, limit)


@app.get("/books/{book_id}", response_model=Book)
async def get_book_endpoint(book_id: int, db: AsyncSession = Depends(get_db)):
    return await get_book(db, book_id)


@app.put("/books/{book_id}", response_model=Book)
async def update_book_endpoint(book_id: int, book: BookUpdate, db: AsyncSession = Depends(get_db)):
    return await update_book(db, book_id, book)


@app.delete("/books/{book_id}")
async def delete_book_endpoint(book_id: int, db: AsyncSession = Depends(get_db)):
    await delete_book(db, book_id)
    return {"message": "Book deleted"}


@app.post("/books/{book_id}/reviews", response_model=Review)
async def create_review_endpoint(book_id: int, review: ReviewCreate, db: AsyncSession = Depends(get_db)):
    return await create_review(db, book_id, review)


@app.get("/books/{book_id}/reviews", response_model=List[Review])
async def get_reviews_endpoint(book_id: int, db: AsyncSession = Depends(get_db)):
    return await get_reviews(db, book_id)


@app.get("/books/{book_id}/summary")
async def get_summary_endpoint(book_id: int, db: AsyncSession = Depends(get_db)):
    return await get_summary(db, book_id)


@app.get("/recommendations")
async def get_recommendations_endpoint(genre: str, rating: float):
    return await get_recommendations(genre, rating)
