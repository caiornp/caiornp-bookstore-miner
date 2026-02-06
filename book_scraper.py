"""Module for scraping book data from http://books.toscrape.com."""

import csv
import re
from pathlib import Path
from typing import List

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel


class Book(BaseModel):
    """Represents a book scraped from the bookstore."""

    title: str
    price: float
    currency: str
    rating: str
    availability: str


def get_currency_code(price_str: str) -> str:
    """Extracts the currency symbol and returns the 3-letter currency code."""
    currency_map = {
        "£": "GBP",
        "$": "USD",
        "€": "EUR",
    }
    for symbol, code in currency_map.items():
        if symbol in price_str:
            return code
    return "UNK"  # Unknown


def parse_book_element(book_element: BeautifulSoup) -> Book:
    """Parses a single book HTML element into a Book model."""
    title = book_element.h3.find("a")["title"]
    price_text = book_element.find("p", class_="price_color").text
    currency = get_currency_code(price_text)
    # Extract numeric price
    price_val = float(re.sub(r"[^\d.]", "", price_text))

    availability_tag = book_element.find("p", class_="instock availability")
    availability = availability_tag.text.strip()
    rating = book_element.find("p", class_="star-rating")["class"][1]

    return Book(
        title=title,
        price=price_val,
        currency=currency,
        rating=rating,
        availability=availability,
    )


def scrape_books() -> None:
    """Scrapes book data from the bookstore and saves it to a CSV file.

    This function connects to the bookstore website, extracts title, price,
    rating, and availability for each book found on the main page,
    validates the data using a Pydantic model, and saves it to CSV.
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
    book_elements = soup.find_all("article", class_="product_pod")
    print(f"Found {len(book_elements)} books. Extracting data...")

    data_to_save: List[Book] = [parse_book_element(be) for be in book_elements]

    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = output_dir / "books_data.csv"
    with filename.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "Price", "Currency", "Rating", "Status"])
        for item in data_to_save:
            writer.writerow(
                [
                    item.title,
                    item.price,
                    item.currency,
                    item.rating,
                    item.availability,
                ]
            )

    print(f"Success! Scraped {len(data_to_save)} books into {filename}")


if __name__ == "__main__":
    scrape_books()
