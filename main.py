from typing import Optional
from fastapi import FastAPI, Body
from pydantic import BaseModel, Field

app = FastAPI()


class BookRequest(BaseModel):
    id: Optional[int] = Field(
        description="The ID of the book, optional for creation.")
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: str
    rating: int = Field(gt=1, lt=5)  # Rating should be between 1 and 5
    # Published date should be a positive integer
    published_date: int = Field(min_length=4, max_length=4)
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "The Great Afia",
                "author": "Mo MO",
                "description": "A story of obsession, wealth, and the American Dream.",
                "rating": 4,
                "published_date": 1925
            }
        }
    }


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


Books = [
    Book(1, "To Kill a Mockingbird", "Harper Lee",
         "A novel about racial injustice in the American South.", 5, 1960),
    Book(2, "1984", "George Orwell",
         "A dystopian novel about totalitarianism and government surveillance.", 5, 1948),
    Book(3, "The Great Gatsby", "F. Scott Fitzgerald",
         "A story of obsession, wealth, and the American Dream.", 4, 1925),
    Book(4, "The Hobbit", "J.R.R. Tolkien",
         "A fantasy novel following the adventures of Bilbo Baggins.", 5, 1937),
    Book(5, "A Brief History of Time", "Stephen Hawking",
         "An explanation of cosmology, black holes, and the Big Bang.", 5, 1998),
    Book(6, "The Catcher in the Rye", "J.D. Salinger",
         "A novel dealing with themes of teenage alienation and loss of innocence.", 4, 1951),
    Book(7, "Pride and Prejudice", "Jane Austen",
         "A romantic masterpiece about love, social class, and reputation.", 4, 1813),
    Book(8, "Sapiens", "Yuval Noah Harari",
         "A groundbreaking narrative on the history of humankind.", 5, 2011),
    Book(9, "The Alchemist", "Paulo Coelho",
         "An allegorical novel about following your dreams and listening to your heart.", 4, 1988),
    Book(10, "Brave New World", "Aldous Huxley",
         "A dystopian vision of a technologically advanced future society.", 4, 1932),
    Book(11, "Crime and Punishment", "Fyodor Dostoevsky",
         "A psychological drama about guilt, morality, and redemption.", 5, 1866),
    Book(12, "Thinking, Fast and Slow", "Daniel Kahneman",
         "An exploration of the two systems that drive the way we think.", 4, 2011),
    Book(13, "The Little Prince", "Antoine de Saint-Exupéry",
         "A philosophical fable about life, love, and human nature.", 5, 1943),
    Book(14, "Dune", "Frank Herbert",
         "The epic sci-fi masterpiece set on the desert planet Arrakis.", 5, 1965),
    Book(15, "Atomic Habits", "James Clear",
         "A practical guide to building good habits and breaking bad ones.", 5, 2018)
]


# ---------------------------------- Fetching books ----------------------------------#

# return books by rating
@app.get("/books/rating")
async def get_books_by_rating(rating: int):
    filtered_books = [book for book in Books if book.rating == rating]
    return filtered_books if filtered_books else {"error": "No books found with the specified rating."}

# return books by published date


@app.get("/books/published_date")
async def get_books_by_published_date(published_date: int):
    filtered_books = [
        book for book in Books if book.published_date == published_date]
    return filtered_books if filtered_books else {"error": "No books found with the specified published date."}

# ---------------------------------- CRUD operations ----------------------------------#


@app.get("/books")
async def read_all_books():
    return Books


@app.get("/books/{book_id}")
async def read_book(book_id: int):
    for book in Books:
        if book.id == book_id:
            return book
    return {"error": "Book not found"}


@app.post("/create_book")
async def create_book(BookRequested: BookRequest):
    newbook = Book(**BookRequested.model_dump())
    print(type(BookRequested))
    Books.append(find_book_id(newbook))
    return newbook


def find_book_id(book: Book):
    book.id = 1 if len(Books) == 0 else Books[-1].id + 1
    return book


@app.put("/update_book")
async def update_book(book: BookRequest):
    for i in range(len(Books)):
        if Books[i].id == book.id:
            Books[i] = Book(**book.model_dump())
            return Books[i]
    return {"error": "Book not found"}


@app.delete("/delete_book/{book_id}")
async def delete_book(book_id: int):
    for i in range(len(Books)):
        if Books[i].id == book_id:
            deleted_book = Books.pop(i)
            return {"message": f"Book with ID {deleted_book.id} has been deleted."}
    return {"error": "Book not found"}
