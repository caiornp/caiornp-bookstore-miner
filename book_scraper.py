import csv
from pathlib import Path
from typing import List

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel


class Book(BaseModel):
    """Represents a book scraped from the bookstore."""

    title: str
    price: str
    rating: str
    availability: str


def scrape_books() -> None:
    """Scrapes book data from http://books.toscrape.com and saves it to a CSV file.

    This function connects to the bookstore website, extracts title, price,
    rating, and availability for each book found on the main page,
    validates the data using a Pydantic model, and saves it to 'books_data.csv'.
    """
    base_url = "http://books.toscrape.com"
    print(f"Connecting to {base_url}...")
    try:
        response = requests.get(base_url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to retrieve the website: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article", class_="product_pod")
    print(f"Found {len(books)} books. Extracting data...")

    data_to_save: List[Book] = []

    for book in books:
        title = book.h3.find("a")["title"]
        price = book.find("p", class_="price_color").text.replace("£", "")
        availability = book.find("p", class_="instock availability").text.strip()
        rating = book.find("p", class_="star-rating")["class"][1]

        # Validate data using Pydantic
        book_data = Book(
            title=title, price=price, rating=rating, availability=availability
        )
        data_to_save.append(book_data)

    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = output_dir / "books_data.csv"
    with filename.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Book Title", "Price", "Rating", "Status"])
        for book_item in data_to_save:
            writer.writerow(
                [
                    book_item.title,
                    book_item.price,
                    book_item.rating,
                    book_item.availability,
                ]
            )

    print(f"Success! Scraped {len(data_to_save)} books into {filename}")


if __name__ == "__main__":
    scrape_books()
