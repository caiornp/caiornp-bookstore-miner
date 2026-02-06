from pathlib import Path
from unittest.mock import MagicMock, patch

from book_scraper import Book, scrape_books


def test_book_model_validation():
    """Test that the Book Pydantic model validates data correctly."""
    data = {
        "title": "A Light in the Attic",
        "price": "51.77",
        "rating": "Three",
        "availability": "In stock",
    }
    book = Book(**data)
    assert book.title == data["title"]
    assert book.price == data["price"]


@patch("book_scraper.requests.get")
def test_scrape_books_success(mock_get):
    """Test successful scraping and CSV creation."""
    # Mock HTML response
    mock_html = """
    <html>
        <body>
            <article class="product_pod">
                <h3><a title="A Light in the Attic">A Light...</a></h3>
                <p class="price_color">£51.77</p>
                <p class="instock availability">
                    <i class="icon-ok"></i> In stock
                </p>
                <p class="star-rating Three"></p>
            </article>
        </body>
    </html>
    """
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = mock_html
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    # Run the scraper
    scrape_books()

    # Check if CSV was created
    csv_file = Path("output/books_data.csv")
    assert csv_file.exists()

    # Verify content
    with csv_file.open("r", encoding="utf-8") as f:
        content = f.read()
        assert "A Light in the Attic" in content
        assert "51.77" in content
        assert "Three" in content

    # Cleanup
    csv_file.unlink()
    # Attempt to remove the directory if empty, but don't fail if not
    try:
        csv_file.parent.rmdir()
    except OSError:
        pass
