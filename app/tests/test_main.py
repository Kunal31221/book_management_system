# app/tests/test_main.py
import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_create_book():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/books", json={"title": "Test Book", "author": "Author", "genre": "Genre",
                                                 "year_published": 2021})
    assert response.status_code == 200
    assert response.json()["title"] == "Test Book"
