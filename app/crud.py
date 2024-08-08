from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException
from app.models import Book, Review
from app.schemas import BookCreate, BookUpdate, ReviewCreate
from app.llama3_integration import generate_summary, generate_review_summary
from app.recommendation import recommend_books


async def create_book(db: AsyncSession, book: BookCreate):
    db_book = Book(title=book.title, author=book.author, genre=book.genre, year_published=book.year_published)
    # Generate summary for the book
    db_book.summary = generate_summary(db_book.title)  # You may need to pass more content to generate a meaningful summary
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return db_book


async def get_books(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(Book).offset(skip).limit(limit))
    return result.scalars().all()


async def get_book(db: AsyncSession, book_id: int):
    try:
        result = await db.execute(select(Book).filter(Book.id == book_id))
        return result.scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Book not found")


async def update_book(db: AsyncSession, book_id: int, book: BookUpdate):
    db_book = await get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in book.dict(exclude_unset=True).items():
        setattr(db_book, key, value)
    await db.commit()
    await db.refresh(db_book)
    return db_book


async def delete_book(db: AsyncSession, book_id: int):
    db_book = await get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    await db.delete(db_book)
    await db.commit()


async def create_review(db: AsyncSession, book_id: int, review: ReviewCreate):
    db_book = await get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db_review = Review(book_id=book_id, **review.dict())
    db.add(db_review)
    await db.commit()
    await db.refresh(db_review)
    return db_review


async def get_reviews(db: AsyncSession, book_id: int):
    result = await db.execute(select(Review).filter(Review.book_id == book_id))
    return result.scalars().all()


async def get_summary(db: AsyncSession, book_id: int):
    book = await get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    reviews = await get_reviews(db, book_id)
    if reviews:
        review_texts = [review.review_text for review in reviews]
        review_summary = generate_review_summary(review_texts)
        average_rating = sum(review.rating for review in reviews) / len(reviews)
    else:
        review_summary = ""
        average_rating = 0
    return {"summary": book.summary, "review_summary": review_summary, "average_rating": average_rating}


async def get_recommendations(genre: str, rating: float):
    return recommend_books(genre, rating)
